from datetime import datetime

from pizza_boom.users.db_models.user_models import UserModel


def update_user_post_confirmation(event: dict) -> UserModel:
    user_attributes: dict = event['request']['userAttributes']
    user_id: str = user_attributes.get('custom:dynamo_user_id')
    user: UserModel = UserModel.get(hash_key=user_id)
    user.update(
        actions=[UserModel.last_sign_in.set(datetime.now())]
    )
    return user
