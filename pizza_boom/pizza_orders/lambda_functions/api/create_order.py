from typing import Any

import structlog

from pizza_boom.core.handlers import LambdaBase, lambda_injector
from pizza_boom.pizza_orders.business_logic.create_pizza_order import (
    create_pizza_order_and_start_execution
)


logger = structlog.get_logger()


class CreatePizzaOrderLambda(LambdaBase):
    def handler(self, event: dict, context: Any):
        logger.debug(
            "start_to_create_pizza_order",
            aws_event=event
        )
        response: dict = create_pizza_order_and_start_execution(
            event=event,
            settings=self._settings
        )
        return response


handler = lambda_injector.get(CreatePizzaOrderLambda).get_handler()
