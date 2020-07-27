import datetime

import backoff
import structlog
from botocore.exceptions import BotoCoreError, ClientError
from pynamodb.exceptions import DoesNotExist

from pizza_boom.core.aws import stepfunctions
from pizza_boom.core.aws.custom_errors import AwsError, TaskTimedOut
from pizza_boom.core.utils import make_response
from pizza_boom.pizza_orders.db_models.pizza_order_models import PizzaOrder, PizzaStatus
from pizza_boom.pizza_orders.schemas.pizza_order import PizzaOrderSchema


logger = structlog.get_logger()


@backoff.on_exception(backoff.constant, interval=1, exception=DoesNotExist, max_time=10)
def receive_pizza_order_and_finish_task(event: dict) -> dict:
    pizza_order_id: str = event["pathParameters"]["pizza_order_id"]

    try:
        pizza_order: PizzaOrder = PizzaOrder.get(pizza_order_id)
    except PizzaOrder.DoesNotExist:
        logger.debug(
            "order_for_receiving_does_not_exist",
            pizza_order_id=pizza_order_id
        )
        return make_response(
            message_body={"message": "Order does not exist"},
            status_code=404
        )

    if not pizza_order.wait_for_receive_pizza_order_token:
        logger.debug(
            "error_of_state_machine_task_or_order",
            error_message="Task does not exist or the order is still being prepared",
            order_id=pizza_order_id,
            order_status=pizza_order.status,
        )
        return make_response(
            message_body={
                "message": "Task does not exist or the order is still being prepared",
            },
            status_code=404
        )

    try:
        stepfunctions.send_task_success(
            task_token=pizza_order.wait_for_receive_pizza_order_token,
            output={"pizza_order_id": pizza_order_id}
        )
    except TaskTimedOut as e:
        logger.error(f"TaskTimeOut: {e}")
        return make_response(message_body={"message": "Task timed out"}, status_code=400)
    except (AwsError, ClientError, BotoCoreError) as e:
        logger.error(f"Failed to send callback to cooking_pizza_order_task. {e}")
        return make_response(
            message_body={"message": "Failed to send callback to pizza_order_task"},
            status_code=400
        )

    pizza_order.update(
        actions=[
            PizzaOrder.delivered_at.set(datetime.datetime.now()),
            PizzaOrder.status.set(PizzaStatus.RECEIVED.value),
            PizzaOrder.wait_for_receive_pizza_order_token.remove()
        ]
    )
    pizza_order.refresh()
    message_body = {
        "message": "Order is delivered successfully",
        "order": PizzaOrderSchema().dump(pizza_order)
    }
    return make_response(message_body=message_body, status_code=200)
