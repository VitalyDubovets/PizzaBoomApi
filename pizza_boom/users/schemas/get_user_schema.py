from marshmallow import Schema, fields


class GetUserSchema(Schema):
    id = fields.Str(required=True)
    email = fields.Email(required=True)
    username = fields.Str(required=True)
    first_name = fields.Str()
    last_name = fields.Str()
    last_sign_in = fields.DateTime(required=True)
    created_at = fields.DateTime(required=True)
    phone = fields.Str()

    class Meta:
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'last_sign_in',
            'created_at',
            'phone'
        )
        ordered = True
