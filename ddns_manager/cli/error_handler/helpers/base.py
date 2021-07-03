from abc import ABC, abstractmethod
from typing import Dict

from ddns_manager.cli.helpers import ConfigHelper
from ddns_manager.error_handler import ErrorHandlerType


class ErrorHandlerConfigHelper(ConfigHelper, ABC):
    @classmethod
    @abstractmethod
    def build(cls, config: Dict) -> ErrorHandlerType:
        raise NotImplementedError
