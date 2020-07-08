import boto3
import structlog

from core.handlers.lambda_base import LambdaBase

logger = structlog.get_logger()


class PreSignUpLambdaTrigger(LambdaBase):
    def handler(self, event, context):
        logger.debug(
            "pre_sign_up_trigger",
            data=event
        )
        event['response']['autoConfirmUser'] = True
        if event['response']['userAttributes'].get('email'):
            event['response']['autoVerifyEmail'] = True
        return event


handler = PreSignUpLambdaTrigger.get_handler()
