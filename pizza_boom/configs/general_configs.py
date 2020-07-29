import logging.config
import os
import sys
from typing import Any

import jmespath
import rapidjson
import structlog
import yaml
from injector import Module, provider, singleton
from structlog.contextvars import merge_contextvars

from pizza_boom.core.utils import merge


class Settings:
    def __init__(self):
        self._values: dict = {}
        config_files: list = ["settings_default.yml", "settings_environment.yml"]

        for config_file in config_files:
            if os.path.exists(config_file):
                with open(config_file) as file:
                    merge(yaml.load(file, Loader=yaml.FullLoader), self._values)

        merge(dict(os.environ), self._values)

    def get_value(self, path: str, required: bool = True) -> Any:
        target_setting = jmespath.search(path, self._values)
        if required and target_setting is None:
            raise ValueError(f"Required setting {path} was not specified")
        return target_setting


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
