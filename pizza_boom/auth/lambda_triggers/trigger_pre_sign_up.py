import boto3
import structlog

from pizza_boom.core.handlers.lambda_base import LambdaBase

logger = structlog.get_logger()


class PreSignUpLambdaTrigger(LambdaBase):
    def handler(self, event, context):
        logger.debug(
            "pre_sign_up_trigger",
            user_data=event['request']['userAttributes'],
            user_pool_id=event['userPoolId'],
            username=event['userName'],

        )
        event['response']['autoConfirmUser'] = True
        if event['request']['userAttributes'].get('email'):
            event['response']['autoVerifyEmail'] = True
        return event


handler = PreSignUpLambdaTrigger.get_handler()
