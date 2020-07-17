from marshmallow import fields, Schema


class PizzaOrderSchema(Schema):
    id = fields.Str(required=True)
    user_id = fields.Str(required=True)
    created_at = fields.DateTime(required=True)
    delivered_at = fields.DateTime()
    address = fields.Str(required=True)
    additional_phone = fields.Str()
    note = fields.Str()
    status = fields.Str(required=True)

    class Meta:
        fields = (
            'id',
            'user_id',
            'address',
            'additional_phone',
            'note',
            'status',
            'delivered_at',
            'created_at',
        )
        ordered = True
