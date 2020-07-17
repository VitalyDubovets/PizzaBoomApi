from typing import Any

import structlog

from pizza_boom.core.handlers import LambdaBase, lambda_injector
from pizza_boom.pizza_orders.business_logic.receive_pizza_order import receive_pizza_order_and_finish_task


logger = structlog.get_logger()


class ReceivePizzaOrderLambda(LambdaBase):
    def handler(self, event: dict, context: Any) -> dict:
        logger.debug(
            "receive_pizza_order",
            data=event
        )
        response: dict = receive_pizza_order_and_finish_task(event)
        return response


handler = lambda_injector.get(ReceivePizzaOrderLambda).get_handler()
