from typing import Any

import backoff
import structlog
from pynamodb.exceptions import DoesNotExist

from pizza_boom.core.handlers import LambdaBase, lambda_injector
from pizza_boom.pizza_orders.db_models.pizza_order_models import PizzaOrder


logger = structlog.get_logger()


class WaitForReceivePizzaOrderLambda(LambdaBase):
    def handler(self, event: dict, context: Any):
        logger.debug(
            "wait_for_receive_pizza_order",
            data=event
        )

        _ = _set_pizza_order_task_token(
            event['pizza_order_id'], event['task_token']
        )


@backoff.on_exception(backoff.constant, interval=1, exception=DoesNotExist, max_time=10)
def _set_pizza_order_task_token(pizza_order_id: str, task_token: str) -> PizzaOrder:
    pizza_order: PizzaOrder = PizzaOrder.get(pizza_order_id)
    pizza_order.update(
        actions=[
            PizzaOrder.wait_for_receive_pizza_order_token.set(task_token)
        ]
    )
    return pizza_order


handler = lambda_injector.get(WaitForReceivePizzaOrderLambda).get_handler()
