from datetime import datetime

import boto3

from pizza_boom.users.db_models.user_models import UserModel
from pizza_boom.users.schemas.user import UserSchemaCreate


def _create_user(event: dict) -> UserModel:
    user_data: dict = {
        "email": event['request']['userAttributes'].get('email'),
        "username": event['userName'],
        "last_sign_in": datetime.now().isoformat(),
        "created_at": datetime.now().isoformat(),
    }
    user: UserModel = UserSchemaCreate().load(data=user_data)
    user.save()
    return user


def create_user_and_update_user_attributes(event: dict) -> UserModel:
    client = boto3.client('cognito-idp')
    user: UserModel = _create_user(event)

    client.admin_update_user_attributes(
        UserPoolId=event['userPoolId'],
        Username=event['userName'],
        UserAttributes=[
            {
                "Name": "custom:dynamo_user_id",
                "Value": user.id
            },
        ]
    )
    return user
