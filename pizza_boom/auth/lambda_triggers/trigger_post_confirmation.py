from datetime import datetime
from typing import Any

import boto3
import structlog

from pizza_boom.core.handlers import LambdaBase
from pizza_boom.users.db_models.user_models import UserModel
from pizza_boom.users.schemas import UserSchemaCreate


logger = structlog.get_logger()


class PostConfirmationLambdaTrigger(LambdaBase):
    def handler(self, event: dict, context: Any) -> dict:
        logger.debug(
            "post_confirmation_trigger",
            trigger_event=event,
        )
        if event['triggerSource'] == 'PostConfirmation_ConfirmSignUp':
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
            logger.debug(
                "user_post_confirmation_save",
                user_id=user.id,
                email_user=user.email,
            )
        return event


def _create_user(event: dict) -> UserModel:
    user_data: dict = {
        "email": event['request']['userAttributes'].get('email'),
        "username": event['userName'],
        "last_sign_in": datetime.now().isoformat(),
        "created_at": datetime.now().isoformat(),
    }
    user: UserModel = UserSchemaCreate().load(data=user_data)
    user.save()
    user.refresh()
    return user


handler = PostConfirmationLambdaTrigger.get_handler()
