from abc import ABC, abstractmethod


class DDNSUpdaterError(Exception):
    pass


class DDNSUpdater(ABC):

    @abstractmethod
    def update_ddns_record(self, ip: str) -> None:
        raise NotImplementedError
