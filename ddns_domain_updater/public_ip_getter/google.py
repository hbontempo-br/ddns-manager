from .base import PublicIPGetter, PublicIPGetterError
from requests import request, Response
from typing import Callable


class GooglePublicIpGetter(PublicIPGetter):

    url = 'https://domains.google.com/checkip'

    def __init__(self, req = request):
        self._req = req

    def get_current_ip(self) -> str:
        resp = self._req(method='get', url=self.__class__.url)
        if resp.status_code != 200:
            raise PublicIPGetterError
        return resp.text


