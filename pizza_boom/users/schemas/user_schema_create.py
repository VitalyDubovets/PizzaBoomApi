from marshmallow import Schema, fields, post_load

from pizza_boom.users.db_models.user_models import UserModel


class UserSchemaCreate(Schema):
    email = fields.Email(required=True)
    username = fields.Str(required=True)
    last_sign_in = fields.DateTime(required=True)
    created_at = fields.DateTime(required=True)

    @post_load
    def make_user(self, data: dict, **kwargs) -> UserModel:
        return UserModel(**data)
