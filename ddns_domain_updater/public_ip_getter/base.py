from abc import ABC, abstractmethod


class PublicIPGetter(ABC):
    class PublicIPGetterError(Exception):
        pass

    @abstractmethod
    def get_current_ip(self) -> str:
        raise NotImplementedError
