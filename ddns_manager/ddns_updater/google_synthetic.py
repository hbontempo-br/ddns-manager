from requests import request
from typing import NoReturn

from .base import DDNSUpdater, DDNSUpdaterError


class GoogleSyntheticDDNSUpdater(DDNSUpdater):
    base_url = "domains.google.com/nic/update"

    def __init__(self, username: str, password: str, hostname: str, req=request):
        self._req = req
        self._username = username
        self._password = password
        self._hostname = hostname

    def update_ddns_record(self, ip: str) -> NoReturn:
        resp = self._req(
            method="post", url=self.__format_address(), params=self.__params(ip)
        )
        if resp.status_code != 200:
            raise DDNSUpdaterError(
                f"Error on Google Synthetic Record update (status code: {resp.status_code})"
            )
        if not (resp.text.startswith("good") or resp.text.startswith("nochg")):
            raise DDNSUpdaterError(
                f"Error on Google Synthetic Record update (text: {resp.text})"
            )

    def __format_address(self):
        return f"https://{self._username}:{self._password}@{self.__class__.base_url}"

    def __params(self, ip: str):
        return {"hostname": self._hostname, "myip": ip}
