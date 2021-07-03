from abc import ABC, abstractmethod
from typing import Dict

from ddns_manager.cli.helpers import ConfigHelper
from ddns_manager.ddns_updater import DDNSUpdater


class DDNSUpdaterConfigHelper(ConfigHelper, ABC):
    @classmethod
    @abstractmethod
    def build(cls, config: Dict) -> DDNSUpdater:
        raise NotImplementedError
