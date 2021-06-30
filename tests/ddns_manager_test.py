import unittest
from typing import Callable, NoReturn
from ddns_manager import DDNSManager
from ddns_manager.ddns_updater import DDNSUpdater
from ddns_manager.public_ip_getter import PublicIPGetter


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
    def __init__(self, update_ddns_record_action: Callable[[str], None]):
        self.__update_ddns_record_action = update_ddns_record_action

    @property
    def update_ddns_record_action(self):
        return self.__update_ddns_record_action

    @update_ddns_record_action.setter
    def update_ddns_record_action(self, action: Callable[[str], None]):
        self.__update_ddns_record_action = action

    def update_ddns_record(self, ip: str) -> NoReturn:
        self.__update_ddns_record_action(ip=ip)


class CallRecorder:
    def __init__(self, return_value):
        self.ret = return_value
        self.args = None
        self.kwargs = None
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count = self.count + 1
        self.args = args
        self.kwargs = kwargs

        return self.ret


class TestDDNSManager(unittest.TestCase):

    def test_current_ip_should_always_be_up_to_date(self):
        # current_ip should mimic value returned on PublicIPGetter#get_current_ip()
        ip1 = 'ip1'
        mock_pig = MockPublicIPGetter(get_current_ip_action=lambda: ip1)
        mock_du = MockDDNSUpdater(update_ddns_record_action=lambda: None)
        pium = DDNSManager(
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
        mc = CallRecorder(whatever)
        mock_pig = MockPublicIPGetter(get_current_ip_action=mc)
        mock_du = MockDDNSUpdater(update_ddns_record_action=lambda: None)

        self.assertEqual(0, mc.count)

        DDNSManager(
            ip_getter=mock_pig,
            ddns_updater=mock_du
        )
        self.assertEqual(1, mc.count)

    def test_is_ddns_update_should_check_if_current_ip_is_equal_to_ddns_ip(self):
        # is_ddns_outdated should return False if current_ip != ddns_ip
        # is_ddns_outdated should return True if current_ip == ddns_ip
        test_ip = 'test_ip'
        pium = DDNSManager(
            ip_getter=MockPublicIPGetter(get_current_ip_action=lambda: test_ip),
            ddns_updater=MockDDNSUpdater(update_ddns_record_action=lambda ip: None)
        )

        self.assertTrue(pium.is_ddns_outdated(update_current_ip=True))
        self.assertEqual(test_ip, pium.current_ip)
        self.assertNotEqual(test_ip, pium.ddns_ip)

        self.assertTrue(pium.is_ddns_outdated(update_current_ip=False))
        self.assertEqual(test_ip, pium.current_ip)
        self.assertNotEqual(test_ip, pium.ddns_ip)

        pium.update_ddns()

        self.assertFalse(pium.is_ddns_outdated(update_current_ip=True))
        self.assertEqual(test_ip, pium.current_ip)
        self.assertEqual(test_ip, pium.ddns_ip)

        self.assertFalse(pium.is_ddns_outdated(update_current_ip=False))
        self.assertEqual(test_ip, pium.current_ip)
        self.assertEqual(test_ip, pium.ddns_ip)

    def test_is_ddns_update_with_update_parameter_should_call_ip_getter(self):
        # is_ddns_outdated with update_current_ip=True should not call PublicIPGetter#get_current_ip()
        test_ip = 'test_ip'
        mock_pig = MockPublicIPGetter(get_current_ip_action=lambda: test_ip)
        mock_du = MockDDNSUpdater(update_ddns_record_action=lambda ip: None)

        pium = DDNSManager(
            ip_getter=mock_pig,
            ddns_updater=mock_du
        )

        test_ip2 = 'test_ip2'
        mc = CallRecorder(test_ip2)
        mock_pig.get_current_ip_action = mc
        self.assertEqual(0, mc.count)

        pium.is_ddns_outdated(update_current_ip=False)
        self.assertEqual(0, mc.count)

        pium.is_ddns_outdated(update_current_ip=True)
        self.assertEqual(1, mc.count)

    def test_ddns_ip_initialization(self):
        # ddns_ip should be initialized with None value
        pium = DDNSManager(
            ip_getter=MockPublicIPGetter(get_current_ip_action=lambda: 'whatever'),
            ddns_updater=MockDDNSUpdater(update_ddns_record_action=lambda ip: None)
        )
        self.assertIsNone(pium.ddns_ip)

    def test_ddns_ip_update_with_update_ip_false(self):
        # ddns_ip should be equal to #current_ip after #update_ddns without a update_current_ip
        test_ip = 'test_ip'
        pium = DDNSManager(
            ip_getter=MockPublicIPGetter(get_current_ip_action=lambda: test_ip),
            ddns_updater=MockDDNSUpdater(update_ddns_record_action=lambda ip: None)
        )
        pium.update_ddns(update_current_ip=False)
        self.assertEqual(test_ip, pium.current_ip)
        self.assertEqual(test_ip, pium.ddns_ip)

    def test_ddns_ip_update_with_update_ip_true(self):
        # ddns_ip should be equal to #current_ip after #update_ddns with a update_current_ip
        test_ip = 'test_ip'
        pium = DDNSManager(
            ip_getter=MockPublicIPGetter(get_current_ip_action=lambda: test_ip),
            ddns_updater=MockDDNSUpdater(update_ddns_record_action=lambda ip: None)
        )
        pium.update_ddns(update_current_ip=True)
        self.assertEqual(test_ip, pium.current_ip)
        self.assertEqual(test_ip, pium.ddns_ip)

    def test_ddns_ip_update_with_update_should_call_public_ip_getter(self):
        # ddns_ip with update_current_ip=True should call PublicIPGetter#get_current_ip()
        test_ip = 'test_ip'
        mock_pig = MockPublicIPGetter(get_current_ip_action=lambda: test_ip)
        mock_du = MockDDNSUpdater(update_ddns_record_action=lambda ip: None)

        pium = DDNSManager(
            ip_getter=mock_pig,
            ddns_updater=mock_du
        )

        test_ip2 = 'test_ip2'
        mc = CallRecorder(test_ip2)
        mock_pig.get_current_ip_action = mc
        self.assertEqual(0, mc.count)

        pium.update_ddns()

        self.assertEqual(1, mc.count)

    def test_ddns_ip_update_without_update_should_not_call_public_ip_getter(self):
        # ddns_ip with update_current_ip=True should call PublicIPGetter#get_current_ip()
        test_ip = 'test_ip'
        mock_pig = MockPublicIPGetter(get_current_ip_action=lambda: test_ip)
        mock_du = MockDDNSUpdater(update_ddns_record_action=lambda ip: None)

        pium = DDNSManager(
            ip_getter=mock_pig,
            ddns_updater=mock_du
        )

        test_ip2 = 'test_ip2'
        mc = CallRecorder(test_ip2)
        mock_pig.get_current_ip_action = mc
        self.assertEqual(0, mc.count)

        pium.update_ddns(update_current_ip=False)

        self.assertEqual(0, mc.count)

    def test_ddns_ip_update_should_call_ddns_updater(self):
        # update_ddns should call DDNSUpdater if ddns ip is not outdated
        mc = CallRecorder(None)
        mock_pig = MockPublicIPGetter(get_current_ip_action=lambda: "whatever")
        mock_du = MockDDNSUpdater(update_ddns_record_action=mc)

        pium = DDNSManager(
            ip_getter=mock_pig,
            ddns_updater=mock_du
        )
        self.assertEqual(0, mc.count)

        self.assertNotEqual(pium.ddns_ip, pium.current_ip)
        pium.update_ddns(update_current_ip=False)
        self.assertEqual(1, mc.count)

        mock_pig.get_current_ip_action = lambda: "another_whatever"
        self.assertNotEqual(pium.ddns_ip, pium.current_ip)
        pium.update_ddns(update_current_ip=True)
        self.assertEqual(2, mc.count)

    def test_ddns_ip_update_should_not_call_ddns_updater_if_ip_has_not_changed(self):
        # update_ddns should not call DDNSUpdater if ddns ip is not outdated
        mc = CallRecorder(None)
        mock_pig = MockPublicIPGetter(get_current_ip_action=lambda: "whatever")
        mock_du = MockDDNSUpdater(update_ddns_record_action=mc)

        pium = DDNSManager(
            ip_getter=mock_pig,
            ddns_updater=mock_du
        )
        self.assertEqual(0, mc.count)

        # ddns ip is outdated, DDNSUpdater is called
        self.assertNotEqual(pium.ddns_ip, pium.current_ip)
        pium.update_ddns(update_current_ip=False)
        self.assertEqual(1, mc.count)

        # ddns ip is not outdated, DDNSUpdater is not called
        self.assertEqual(pium.ddns_ip, pium.current_ip)
        pium.update_ddns(update_current_ip=True)
        self.assertEqual(1, mc.count)
