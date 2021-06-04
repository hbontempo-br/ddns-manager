from ddns_domain_updater.public_ip_getter import PublicIPGetter
from ddns_domain_updater.ddns_updater import DDNSUpdater


class PublicIpUpdateManager:
    def __init__(self, ip_getter: PublicIPGetter, ddns_updater: DDNSUpdater):
        self._ddns_updater = ddns_updater
        self._ip_getter = ip_getter
        self._current_ip = None
        self.__update_current_ip()
        self._ddns_ip = None

    @property
    def current_ip(self):
        self.__update_current_ip()
        return self._current_ip

    @property
    def ddns_ip(self):
        return self._ddns_ip

    def is_ddns_outdated(self, update_current_ip: bool = True):
        if update_current_ip:
            self.__update_current_ip()
        return self._ddns_ip != self._current_ip

    def update_ddns(self, update_current_ip: bool = True):
        if self.is_ddns_outdated(update_current_ip=update_current_ip):
            self.__update_ddns()

    def __update_current_ip(self):
        self._current_ip = self._ip_getter.get_current_ip()

    def __update_ddns(self):
        self._ddns_updater.update_ddns_record(ip=self._current_ip)
        self._ddns_ip = self._current_ip
