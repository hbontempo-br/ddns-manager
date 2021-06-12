from .base import PublicIPGetter, PublicIPGetterError
from requests import get, Response
from typing import Callable


class GooglePublicIpGetter(PublicIPGetter):

    url = 'https://domains.google.com/checkip'

    def __init__(self, getter: Callable[[str], Response] = get):
        self._getter = getter

    def get_current_ip(self) -> str:
        resp = self._getter(self.__class__.url)
        if resp.status_code != 200:
            raise PublicIPGetterError
        return resp.text


