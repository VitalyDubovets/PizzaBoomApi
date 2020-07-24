from typing import Any

import structlog

from pizza_boom.auth.business_logic.create_user import (
    create_user_and_update_user_attributes
)
from pizza_boom.core.handlers import LambdaBase, lambda_injector
from pizza_boom.users.db_models.user_models import UserModel


logger = structlog.get_logger()


class PostConfirmationLambdaTrigger(LambdaBase):
    def handler(self, event: dict, context: Any) -> dict:
        logger.debug(
            "post_confirmation_trigger",
            trigger_event=event,
        )
        if event['triggerSource'] == 'PostConfirmation_ConfirmSignUp':
            user: UserModel = create_user_and_update_user_attributes(event)

            logger.debug(
                "user_post_confirmation_save",
                user_id=user.id,
                email_user=user.email,
            )
        return event


handler = lambda_injector.get(PostConfirmationLambdaTrigger).get_handler()
