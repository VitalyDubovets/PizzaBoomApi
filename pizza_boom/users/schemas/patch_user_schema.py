from marshmallow import Schema, fields


class PatchUserSchema(Schema):
    first_name = fields.Str()
    last_name = fields.Str()
    phone = fields.Str()
