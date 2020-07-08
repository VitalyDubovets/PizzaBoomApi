from abc import ABC, abstractmethod

import structlog

from configs import configure_logging


class LambdaBase(ABC):
    def __init__(self):
        configure_logging()
        self.logger = structlog.getLogger(f"lambda_function.{self.__class__.__name__}")