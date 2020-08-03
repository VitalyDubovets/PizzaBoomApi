import logging.config
import sys

import rapidjson
import structlog
from injector import Module, provider, singleton
from pydantic import Extra
from structlog.contextvars import merge_contextvars

from pizza_boom.core.settings.custom_settings import CustomSettings


class Settings(CustomSettings):
    AWS_PROFILE: str
    AWS_REGION: str
    API_VERSION: str
    DOMAIN: str
    PREFIX_TABLE: str
    PIZZA_ORDER_STATE_MACHINE_ARN: str = None
    STAGE: str = None

    class Config:
        env_file = '.env'
        yaml_file = 'settings_default.yml'
        extra = Extra.ignore
        case_sensitive = True


class SettingsModule(Module):
    @singleton
    @provider
    def provide_settings(self) -> Settings:
        return Settings()


def configure_logging(log_format: str = 'json'):
    root_logger = logging.getLogger()
    root_logger.handlers = []

    logging.basicConfig(format="%(message)s", stream=sys.stdout, level=logging.DEBUG)

    if log_format == 'json':
        renderer = structlog.processors.JSONRenderer(serializer=rapidjson.dumps)
    else:
        renderer = structlog.dev.ConsoleRenderer()

    structlog.configure(
        processors=[
            merge_contextvars,
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.format_exc_info,
            renderer,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        context_class=dict,
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
