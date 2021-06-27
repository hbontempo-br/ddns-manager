from abc import ABC, abstractmethod
from typing import Dict


class ConfigHelper(ABC):

    @classmethod
    @abstractmethod
    def build(cls, config: Dict):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def new_config() -> Dict:
        raise NotImplementedError
