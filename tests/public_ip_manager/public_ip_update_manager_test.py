import unittest
from typing import Callable
from ddns_domain_updater.public_ip_update_manager import PublicIpUpdateManager
from ddns_domain_updater.ddns_updater import DDNSUpdater
from ddns_domain_updater.public_ip_getter import PublicIPGetter


class MockPublicIPGetter(PublicIPGetter):

    def __init__(self, get_current_ip_action: Callable[[], str]):
        self.__get_current_ip_action = get_current_ip_action

    @property
    def get_current_ip_action(self):
        return self.__get_current_ip_action

    @get_current_ip_action.setter
    def get_current_ip_action(self, action: Callable[[], str]):
        self.__get_current_ip_action = action

    def get_current_ip(self) -> str:
        return self.__get_current_ip_action()


class MockDDNSUpdater(DDNSUpdater):
    def __init__(self, update_ddns_record_action: Callable[[], None]):
        self.__update_ddns_record_action = update_ddns_record_action

    @property
    def update_ddns_record_action(self):
        return self.__update_ddns_record_action

    @update_ddns_record_action.setter
    def update_ddns_record_action(self, action: Callable[[], None]):
        self.__update_ddns_record_action = action

    def update_ddns_record(self, ip: str) -> None:
        self.__update_ddns_record_action()


class MethodCounter:
    def __init__(self, return_value):
        self.ret = return_value
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count = self.count + 1
        return self.ret


class TestPublicIpUpdateManager(unittest.TestCase):

    # Scenarios:
    #   - #current_ip should not change if exception is raise on PublicIPGetter#get_current_ip()
    #   - #ddns_ip should be initialized with None value
    #   - #ddns_ip should be equal to #current_ip after #update_ddns (with or without a update_current_ip)
    #   - #ddns_ip with update_current_ip=True should call PublicIPGetter#get_current_ip()
    #   - #update_ddns with update_current_ip=False should not call PublicIPGetter#get_current_ip()
    #   - #update_ddns with update_current_ip=False should call DDNSUpdater#update_ddns_record(ip) with ip = current_ip
    #   - #update_ddns should not change ddns_ip if DDNSUpdater#update_ddns_record(ip) raises error
    #   - #update_ddns with should not change ddns_ip if PublicIPGetter#get_current_ip() raises error
    #   - #is_ddns_outdated should return True if current_ip == ddns_ip
    #   - #is_ddns_outdated should return False if current_ip != ddns_ip
    #   - #is_ddns_outdated with update_current_ip=True should not call PublicIPGetter#get_current_ip()

    def test_current_ip_should_always_be_up_to_date(self):
        # current_ip should mimic value returned on PublicIPGetter#get_current_ip()
        ip1 = 'ip1'
        mock_pig = MockPublicIPGetter(get_current_ip_action=lambda: ip1)
        mock_du = MockDDNSUpdater(update_ddns_record_action=lambda: None)
        pium = PublicIpUpdateManager(
            ip_getter=mock_pig,
            ddns_updater=mock_du
        )
        self.assertEqual(ip1, pium.current_ip)

        ip2 = 'ip2'
        mock_pig.get_current_ip_action = lambda: ip2
        self.assertEqual(ip2, pium.current_ip)

    def test_current_ip_should_call_public_ip_getter(self):
        # current_ip should call PublicIPGetter#get_current_ip()
        whatever = 'whatever'
        mc = MethodCounter(whatever)
        mock_pig = MockPublicIPGetter(get_current_ip_action=mc)
        mock_du = MockDDNSUpdater(update_ddns_record_action=lambda: None)

        self.assertEqual(0, mc.count)

        PublicIpUpdateManager(
            ip_getter=mock_pig,
            ddns_updater=mock_du
        )
        self.assertEqual(1, mc.count)
