import logging.config
import sys

import rapidjson
import structlog
from structlog.contextvars import merge_contextvars


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
