from marshmallow import Schema, fields, post_load

from pizza_boom.users.db_models.user_models import UserModel


class UserSchemaCreate(Schema):
    email = fields.Email(required=True)
    username = fields.Email(required=True)

    @post_load
    def make_user(self, data: dict, **kwargs) -> UserModel:
        return UserModel(**data)
