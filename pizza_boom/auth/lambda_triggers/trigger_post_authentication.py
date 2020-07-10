from datetime import datetime
from typing import Any

import boto3
import structlog

from pizza_boom.core.handlers import LambdaBase
from pizza_boom.users.db_models.user_models import UserModel


logger = structlog.get_logger()


class PostAuthenticationLambdaTrigger(LambdaBase):
    def handler(self, event: dict, context: Any) -> dict:
        logger.debug(
            "post_authentication_trigger",
            trigger_event=event
        )
        if event['triggerSource'] == "PostAuthentication_Authentication":
            user_attributes: dict = event['request']['userAttributes']
            user_id: str = user_attributes.get('custom:dynamo_user_id')
            user: UserModel = UserModel.get(hash_key=user_id)
            user.update(
                actions=[UserModel.last_sign_in.set(datetime.now())]
            )
        return event


handler = PostAuthenticationLambdaTrigger.get_handler()
