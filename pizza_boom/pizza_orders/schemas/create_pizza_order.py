from marshmallow import fields, post_load, Schema

from pizza_boom.pizza_orders.db_models.pizza_order_models import PizzaOrder


class PizzaOrderCreateSchema(Schema):
    address = fields.Str(required=True)
    additional_phone = fields.Str()
    note = fields.Str()

    @post_load
    def make_pizza_order(self, data: dict, **kwargs) -> PizzaOrder:
        return PizzaOrder(**data)
