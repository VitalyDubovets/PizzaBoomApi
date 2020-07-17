from typing import Any

import structlog

from pizza_boom.core.handlers import LambdaBase, lambda_injector
from pizza_boom.pizza_orders.business_logic.quality import checking_the_quality


logger = structlog.get_logger()


class EvaluateQualityLambda(LambdaBase):
    def handler(self, event: dict, context: Any) -> dict:
        event: dict = checking_the_quality(event)
        logger.debug(
            "evaluate_quality",
            data=event
        )
        return event


handler = lambda_injector.get(EvaluateQualityLambda).get_handler()
