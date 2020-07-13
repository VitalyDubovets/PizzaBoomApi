from pizza_boom.users.db_models.user_models import UserModel
from pizza_boom.users.errors import NotFoundRequestDataError, UserNotFoundError
from pizza_boom.users.schemas import GetUserSchema


def patch_user(user_id: str, user_patch_data: dict) -> dict:
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
