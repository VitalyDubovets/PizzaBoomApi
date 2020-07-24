from typing import Any

import structlog

from pizza_boom.auth.business_logic.custom_message import form_email_message
from pizza_boom.core.handlers import LambdaBase, lambda_injector


logger = structlog.get_logger()


class CustomMessageLambdaTrigger(LambdaBase):
    def handler(self, event: dict, context: Any) -> dict:
        logger.debug(
            "custom_message_trigger",
            trigger_event=event
        )
        if event['triggerSource'] == "CustomMessage_SignUp":
            event: dict = form_email_message(event)
        return event


handler = lambda_injector.get(CustomMessageLambdaTrigger).get_handler()
