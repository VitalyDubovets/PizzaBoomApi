from marshmallow import fields, post_load, Schema

from pizza_boom.pizza_orders.db_models.pizza_order_models import PizzaOrder


class BasePizzaOrderSchema(Schema):
    id = fields.Str()
    user_id = fields.Str()
    created_at = fields.DateTime()
    delivered_at = fields.DateTime()
    address = fields.Str()
    additional_phone = fields.Str()
    note = fields.Str()
    status = fields.Str()

    class Meta:
        ordered = True


class PizzaOrderCreateSchema(BasePizzaOrderSchema):
    address = fields.Str(required=True)

    @post_load
    def make_pizza_order(self, data: dict, **kwargs) -> PizzaOrder:
        return PizzaOrder(**data)

    class Meta:
        fields = (
            'address',
            'additional_phone',
            'note',
        )


class PizzaOrderSchema(BasePizzaOrderSchema):
    pass
