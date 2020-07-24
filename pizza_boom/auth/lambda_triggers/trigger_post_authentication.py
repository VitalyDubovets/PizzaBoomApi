from typing import Any

import structlog

from pizza_boom.auth.business_logic.update_user import update_user_post_confirmation
from pizza_boom.core.handlers import LambdaBase, lambda_injector


logger = structlog.get_logger()


class PostAuthenticationLambdaTrigger(LambdaBase):
    def handler(self, event: dict, context: Any) -> dict:
        logger.debug(
            "post_authentication_trigger",
            trigger_event=event
        )
        if event['triggerSource'] == "PostAuthentication_Authentication":
            _ = update_user_post_confirmation(event)
        return event


handler = lambda_injector.get(PostAuthenticationLambdaTrigger).get_handler()
