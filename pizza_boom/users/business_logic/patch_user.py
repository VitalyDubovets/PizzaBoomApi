import marshmallow

from pizza_boom.users.db_models.user_models import UserModel
from pizza_boom.users.errors import NotFoundRequestDataError, UserNotFoundError
from pizza_boom.users.schemas import GetUserSchema, PatchUserSchema


def patch_user(user_id: str, json_data: dict) -> dict:
    patch_schema: PatchUserSchema = PatchUserSchema(unknown=marshmallow.EXCLUDE)
    user_patch_data: dict = patch_schema.load(json_data)

    if not user_patch_data:
        raise NotFoundRequestDataError

    schema: GetUserSchema = GetUserSchema()
    try:
        user: UserModel = UserModel.get(user_id)
    except UserModel.DoesNotExist:
        raise UserNotFoundError

    user.update(actions=[
        getattr(UserModel, attr).set(value) for attr, value in user_patch_data.items()
    ])
    user.refresh()

    return schema.dump(user)
