from abc import ABC, abstractmethod


class DDNSUpdater(ABC):
    class DDNSUpdaterError(Exception):
        pass

    @abstractmethod
    def update_ddns_record(self, ip: str) -> None:
        raise NotImplementedError
