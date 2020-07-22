import structlog

from pizza_boom.pizza_orders.db_models.pizza_order_models import PizzaOrder, PizzaStatus


logger = structlog.get_logger()


def pizza_order_failed(pizza_order_id: str, error: str, cause: str):
    logger.debug(
        "pizza_order_failed",
        pizza_order_id=pizza_order_id,
        error=error,
        cause=cause,
    )

    pizza_order: PizzaOrder = PizzaOrder.get(pizza_order_id)
    pizza_order.update(
        actions=[PizzaOrder.status.set(PizzaStatus.FAILED.value)]
    )


