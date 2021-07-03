from typing import Dict

from .base import ErrorHandlerConfigHelper
from ddns_manager.error_handler import ErrorHandlerType, retry_handler


class RetryConfigHelper(ErrorHandlerConfigHelper):
    @classmethod
    def build(cls, config: Dict) -> ErrorHandlerType:
        return retry_handler()

    @staticmethod
    def new_config():
        return None
