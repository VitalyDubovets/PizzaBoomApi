import boto3
import structlog
from botocore.exceptions import ClientError
from typing import Any

from pizza_boom.core.handlers.lambda_base import LambdaBase
from pizza_boom.users.db_models.user_models import UserModel

logger = structlog.get_logger()


class PreSignUpLambdaTrigger(LambdaBase):
    def handler(self, event: dict, context: Any) -> dict:
        logger.debug(
            "pre_sign_up_trigger",
            user_data=event['request']['userAttributes'],
            user_pool_id=event['userPoolId'],
            username=event['userName'],
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
            event['response']['autoConfirmUser'] = True
        return event


def _is_email_already_exist(
        email: str, cognito_client: Any, user_pool: str
) -> bool:
    try:
        cognito_client.admin_get_user(UserPoolId=user_pool, Username=email)
        return True
    except ClientError:
        return False


handler = PreSignUpLambdaTrigger.get_handler()
