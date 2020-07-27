from typing import List

from pizza_boom.pizza_orders.db_models.pizza_order_models import PizzaOrder, PizzaStatus
from pizza_boom.pizza_orders.schemas.pizza_order import PizzaOrderSchema


def get_pizza_orders_with_query_params(query_params: dict):
    limit: str = query_params.get('limit') if query_params.get('limit') else None
    status: str = (
        query_params.get('status') if query_params.get('status') else PizzaStatus.RECEIVED
    )

    if limit and isinstance(limit, str):
        limit: int = int(limit)

    pizza_orders: List[PizzaOrder] = [
        item for item in PizzaOrder.scan(PizzaOrder.status == status, limit=limit)
    ]
    pizza_orders_data: dict = PizzaOrderSchema().dump(pizza_orders, many=True)

    return pizza_orders_data, 200
