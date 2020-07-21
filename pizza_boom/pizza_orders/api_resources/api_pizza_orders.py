from typing import List, OrderedDict

import flask
import structlog
from flask_restful import Resource

from pizza_boom.pizza_orders.db_models.pizza_order_models import PizzaOrder, PizzaStatus
from pizza_boom.pizza_orders.schemas.pizza_order import PizzaOrderSchema


logger = structlog.get_logger()


class PizzaOrdersAPI(Resource):
    """
    Endpoint fot getting all pizza orders

    /api/v1/pizza-orders

    method: GET
    """
    @staticmethod
    def get():
        logger.debug(
            "get_pizza_orders",
            query_params=flask.request.args
        )

        query_params: dict = flask.request.args
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
