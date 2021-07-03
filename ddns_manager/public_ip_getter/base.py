from abc import ABC, abstractmethod


class PublicIPGetterError(Exception):
    pass


class PublicIPGetter(ABC):
    @abstractmethod
    def get_current_ip(self) -> str:
        raise NotImplementedError
