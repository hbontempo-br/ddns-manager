from .base import DDNSUpdater, DDNSUpdaterError
from requests import request


class GoogleSyntheticDDNSUpdater(DDNSUpdater):
    base_url = 'domains.google.com/nic/update'

    def __init__(self, username: str, password: str, hostname: str, req=request):
        self._req = req
        self._username = username
        self._password = password
        self._hostname = hostname

    def update_ddns_record(self, ip: str) -> None:
        resp = self._req(method='post', url=self._format_address(), params=self._params(ip))
        if resp.status_code != 200:
            raise DDNSUpdaterError
        if not (resp.text.startswith('good') or resp.text.startswith('nochg')):
            raise DDNSUpdaterError

    def _format_address(self):
        return f"https://{self._username}:{self._password}@{self.__class__.base_url}"

    def _params(self, ip: str):
        return {
            'hostname': self._hostname,
            'myip': ip
        }
