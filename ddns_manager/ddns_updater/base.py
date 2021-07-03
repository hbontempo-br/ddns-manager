from abc import ABC, abstractmethod
from typing import NoReturn


class DDNSUpdaterError(Exception):
    pass


class DDNSUpdater(ABC):
    @abstractmethod
    def update_ddns_record(self, ip: str) -> NoReturn:
        raise NotImplementedError
