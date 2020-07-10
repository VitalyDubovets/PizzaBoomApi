from typing import Any

import structlog

from pizza_boom.core.handlers import LambdaBase


logger = structlog.get_logger()


class CustomMessageLambdaTrigger(LambdaBase):
    def handler(self, event: dict, context: Any) -> dict:
        logger.debug(
            "custom_message_trigger",
            trigger_event=event
        )
        if event['triggerSource'] == "CustomMessage_SignUp":
            event['request']['usernameParameter'] = event['userName']
            event: dict = _form_email_message(event)
        return event


def _form_email_message(event: dict) -> dict:
    event['response']['emailSubject'] = "Добро пожаловать в PizzaBoom"
    event['response']['emailMessage'] = f"""
        Добро пожаловать в PizzaBoom. Ваше имя пользователя: {event['request']['usernameParameter']}.
        Временный код для подтверждения email адреса: {event['request']['codeParameter']}
    """
    return event


handler = CustomMessageLambdaTrigger.get_handler()
