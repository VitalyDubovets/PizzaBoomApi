import flask
import structlog
from flask_restful import Resource

from pizza_boom.pizza_orders.business_logic.get_pizza_order import (
    get_pizza_orders_with_query_params
)


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
        response, status_code = get_pizza_orders_with_query_params(
            query_params=query_params
        )
        return response, status_code
