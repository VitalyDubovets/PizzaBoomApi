import json

import structlog
from marshmallow.exceptions import ValidationError

from pizza_boom.configs import Settings
from pizza_boom.core.aws import stepfunctions
from pizza_boom.core.utils import make_response
from pizza_boom.pizza_orders.db_models.pizza_order_models import PizzaOrder
from pizza_boom.pizza_orders.schemas.pizza_order import PizzaOrderCreateSchema, PizzaOrderSchema
from pizza_boom.users.utils import get_cognito_user_data


logger = structlog.get_logger()


def create_pizza_order_and_start_execution(
        event: dict, settings: Settings
) -> dict:
    try:
        pizza_order = _create_pizza_order(event)
    except ValidationError:
        return make_response(
            message_body={'message': 'Address is empty'}, status_code=400
        )

    execution_arn: str = _start_pizza_order_state_machine(
        pizza_order_id=pizza_order.id,
        settings=settings
    )

    pizza_order.update(actions=[PizzaOrder.execution_arn.set(execution_arn)])
    message_body = {
        'message': 'Order is created',
        'order': PizzaOrderSchema().dump(pizza_order)
    }
    return make_response(message_body=message_body, status_code=201)


def _create_pizza_order(event: dict) -> PizzaOrder:
    user_data: dict = get_cognito_user_data(event)
    logger.debug(
        "create_pizza_order",
        user_data=user_data,
        body=json.loads(event['body'])
    )
    pizza_order: PizzaOrder = PizzaOrderCreateSchema().loads(event['body'])
    pizza_order.user_id = user_data.get('custom:dynamo_user_id')
    pizza_order.save()
    return pizza_order


def _start_pizza_order_state_machine(
    pizza_order_id: str, settings: Settings
) -> str:
    pizza_order_state_machine_arn = settings.PIZZA_ORDER_STATE_MACHINE_ARN
    response: dict = stepfunctions.start_execution(
        state_machine_arn=pizza_order_state_machine_arn,
        input_=dict(pizza_order_id=pizza_order_id),
        name=f"pizza_order_id-{pizza_order_id}",
    )

    logger.debug(
        "Pizza order state machine started",
        response=response,
    )

    execution_arn: str = response["executionArn"]
    return execution_arn
