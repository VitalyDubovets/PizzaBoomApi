from marshmallow import Schema, fields


class PatchUserSchema(Schema):
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    phone = fields.Str(required=True)
