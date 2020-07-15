import uuid
from abc import ABC, abstractmethod

import structlog
from injector import inject, Injector
from structlog.contextvars import bind_contextvars, clear_contextvars

from pizza_boom.configs import configure_logging, Settings, SettingsModule

__all__ = [
    'LambdaBase',
    'lambda_injector'
]


class LambdaBase(ABC):
    @inject
    def __init__(self, settings: Settings):
        configure_logging()
        self.logger = structlog.getLogger(f"lambda_function.{self.__class__.__name__}")

    def get_handler(self):
        def handler(event, context):
            if isinstance(event, dict) and event.get("source") in [
                "aws.events",
                "serverless-plugin-warmup",
            ]:
                self.logger.debug("Lambda warmed up")
                return {}
            clear_contextvars()
            bind_contextvars(request_id=str(uuid.uuid4()))

            return self.handler(event=event, context=context)

        return handler

    @abstractmethod
    def handler(self, event, context):
        ...


lambda_injector = Injector(
    [
        SettingsModule
    ]
)
