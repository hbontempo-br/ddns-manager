from abc import ABC, abstractmethod
from typing import Dict

from ddns_manager.cli.helpers import ConfigHelper
from ddns_manager.public_ip_getter import PublicIPGetter


class PublicIpGetterConfigHelper(ConfigHelper, ABC):
    @classmethod
    @abstractmethod
    def build(cls, config: Dict) -> PublicIPGetter:
        raise NotImplementedError
