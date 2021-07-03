from requests import request

from .base import PublicIPGetter, PublicIPGetterError


class GooglePublicIpGetter(PublicIPGetter):
    base_url = "https://domains.google.com/checkip"

    def __init__(self, req=request):
        self._req = req

    def get_current_ip(self) -> str:
        resp = self._req(method="get", url=self.__class__.base_url)
        if resp.status_code != 200:
            raise PublicIPGetterError(
                f"Error on Google check_ip service (status code: {resp.status_code})"
            )
        return resp.text
