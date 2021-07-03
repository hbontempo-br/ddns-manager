import logging
import time
from typing import Callable

from ddns_manager.ddns_updater import DDNSUpdater
from ddns_manager.public_ip_getter import PublicIPGetter


class DDNSManager:
    def __init__(self, ip_getter: PublicIPGetter, ddns_updater: DDNSUpdater):
        self.__ddns_updater = ddns_updater
        self.__ip_getter = ip_getter
        self.__current_ip = None
        self.__update_current_ip()
        self.__ddns_ip = None

    @property
    def current_ip(self):
        self.__update_current_ip()
        return self.__current_ip

    @property
    def ddns_ip(self):
        return self.__ddns_ip

    def is_ddns_outdated(self, update_current_ip: bool = True):
        if update_current_ip:
            self.__update_current_ip()
        return self.__ddns_ip != self.__current_ip

    def update_ddns(self, update_current_ip: bool = True):
        if self.is_ddns_outdated(update_current_ip=update_current_ip):
            self.__update_ddns()

    def update_loop(self, interval: int, on_error: Callable[[Exception], None]):
        while True:
            try:
                logging.info("Starting new update routine.")
                self.update_ddns(update_current_ip=True)
            except Exception as e:
                on_error(e)
            finally:
                time.sleep(interval)

    def __update_current_ip(self):
        self.__current_ip = self.__ip_getter.get_current_ip()

    def __update_ddns(self):
        self.__ddns_updater.update_ddns_record(ip=self.__current_ip)
        self.__ddns_ip = self.__current_ip
