from typing import Any

import backoff
import structlog
from pynamodb.exceptions import DoesNotExist

from pizza_boom.core.handlers import LambdaBase, lambda_injector
from pizza_boom.pizza_orders.db_models.pizza_order_models import PizzaOrder, PizzaStatus


logger = structlog.get_logger()


class FailReceivePizzaOrderLambda(LambdaBase):
    def handler(self, event: dict, context: Any):
        logger.debug(
            "fail_receive_pizza_order",
            data=event
        )

        _ = _fail_receive_order(event)


handler = lambda_injector.get(FailReceivePizzaOrderLambda).get_handler()


@backoff.on_exception(backoff.constant, interval=1, exception=DoesNotExist, max_time=10)
def _fail_receive_order(event: dict) -> PizzaOrder:
    pizza_order_id: str = event['pizza_order_id']
    pizza_order: PizzaOrder = PizzaOrder.get(pizza_order_id)
    pizza_order.update(
        actions=[PizzaOrder.status.set(PizzaStatus.NOT_RECEIVED.value)]
    )
    return pizza_order
