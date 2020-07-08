import uuid
from abc import ABC, abstractmethod

import structlog
from structlog.contextvars import bind_contextvars, clear_contextvars

from configs import configure_logging


class LambdaBase(ABC):
    def __init__(self):
        configure_logging()
        self.logger = structlog.getLogger(f"lambda_function.{self.__class__.__name__}")

    @classmethod
    def get_handler(cls, *args, **kwargs):
        def handler(event, context):
            if isinstance(event, dict) and event.get("source") in [
                "aws.events",
                "serverless-plugin-warmup",
            ]:
                cls().logger.debug("Lambda warmed up")
                return {}
            clear_contextvars()
            bind_contextvars(request_id=str(uuid.uuid4()))

            return cls().handler(event=event, context=context)

        return handler

    @abstractmethod
    def handler(self, event, context):
        ...
