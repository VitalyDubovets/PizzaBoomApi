from marshmallow import Schema, fields, post_load

from pizza_boom.users.db_models.user_models import UserModel


class BaseUserSchema(Schema):
    id = fields.Str()
    email = fields.Email()
    username = fields.Str()
    first_name = fields.Str()
    last_name = fields.Str()
    last_sign_in = fields.DateTime()
    created_at = fields.DateTime()
    phone = fields.Str()

    class Meta:
        ordered = True


class UserSchemaCreate(BaseUserSchema):
    email = fields.Email(required=True)
    username = fields.Str(required=True)
    last_sign_in = fields.DateTime(required=True)
    created_at = fields.DateTime(required=True)

    @post_load
    def make_user(self, data: dict, **kwargs) -> UserModel:
        return UserModel(**data)

    class Meta:
        fields = (
            'email',
            'username',
            'last_sign_in',
            'created_at',
        )


class GetUserSchema(BaseUserSchema):
    pass


class PatchUserSchema(BaseUserSchema):
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    phone = fields.Str(required=True)

    class Meta:
        fields = (
            'first_name',
            'last_name',
            'phone'
        )
