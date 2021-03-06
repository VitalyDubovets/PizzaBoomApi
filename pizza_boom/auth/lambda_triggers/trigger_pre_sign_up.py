from typing import Any

import boto3
import structlog
from botocore.exceptions import ClientError

from pizza_boom.core.handlers import LambdaBase, lambda_injector


logger = structlog.get_logger()


class PreSignUpLambdaTrigger(LambdaBase):
    def handler(self, event: dict, context: Any) -> dict:
        logger.debug(
            "pre_sign_up_trigger",
            trigger_event=event,
        )
        if event['triggerSource'] == "PreSignUp_SignUp":
            email = event['request']['userAttributes'].get('email')
            client = boto3.client('cognito-idp')
            if email and _is_email_already_exist(
                    email=email,
                    cognito_client=client,
                    user_pool=event['userPoolId']
            ):
                raise Exception('User is already exist')
        return event


def _is_email_already_exist(
        email: str, cognito_client: Any, user_pool: str
) -> bool:
    try:
        cognito_client.admin_get_user(UserPoolId=user_pool, Username=email)
        return True
    except ClientError:
        return False


handler = lambda_injector.get(PreSignUpLambdaTrigger).get_handler()
