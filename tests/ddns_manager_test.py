import unittest
from datetime import datetime, timedelta
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
    def __init__(self, on_call):
        self.on_call = on_call
        self.calls = []

    def __call__(self, *args, **kwargs):
        try:
            response = self.on_call()
            self.calls.append(
                {
                    "args": args,
                    "kwargs": kwargs,
                    "timestamp": datetime.now(),
                    "response": response,
                }
            )
        except Exception as e:
            self.calls.append(
                {
                    "args": args,
                    "kwargs": kwargs,
                    "timestamp": datetime.now(),
                    "exception": e,
                }
            )
            raise e
        return response

    @property
    def count(self):
        return len(self.calls)


class TestDDNSManager(unittest.TestCase):
    def test_current_ip_should_always_be_up_to_date(self):
        # current_ip should mimic value returned on PublicIPGetter#get_current_ip()
        ip1 = "ip1"
        mock_pig = MockPublicIPGetter(get_current_ip_action=lambda: ip1)
        mock_du = MockDDNSUpdater(update_ddns_record_action=lambda: None)
        pium = DDNSManager(ip_getter=mock_pig, ddns_updater=mock_du)
        self.assertEqual(ip1, pium.current_ip)

        ip2 = "ip2"
        mock_pig.get_current_ip_action = lambda: ip2
        self.assertEqual(ip2, pium.current_ip)

    def test_current_ip_should_call_public_ip_getter(self):
        # current_ip should call PublicIPGetter#get_current_ip()
        whatever = "whatever"
        mc = CallRecorder(on_call=lambda: whatever)
        mock_pig = MockPublicIPGetter(get_current_ip_action=mc)
        mock_du = MockDDNSUpdater(update_ddns_record_action=lambda: None)

        self.assertEqual(0, mc.count)

        DDNSManager(ip_getter=mock_pig, ddns_updater=mock_du)
        self.assertEqual(1, mc.count)

    def test_is_ddns_update_should_check_if_current_ip_is_equal_to_ddns_ip(self):
        # is_ddns_outdated should return False if current_ip != ddns_ip
        # is_ddns_outdated should return True if current_ip == ddns_ip
        test_ip = "test_ip"
        pium = DDNSManager(
            ip_getter=MockPublicIPGetter(get_current_ip_action=lambda: test_ip),
            ddns_updater=MockDDNSUpdater(update_ddns_record_action=lambda ip: None),
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
        test_ip = "test_ip"
        mock_pig = MockPublicIPGetter(get_current_ip_action=lambda: test_ip)
        mock_du = MockDDNSUpdater(update_ddns_record_action=lambda ip: None)

        pium = DDNSManager(ip_getter=mock_pig, ddns_updater=mock_du)

        test_ip2 = "test_ip2"
        mc = CallRecorder(on_call=lambda: test_ip2)
        mock_pig.get_current_ip_action = mc
        self.assertEqual(0, mc.count)

        pium.is_ddns_outdated(update_current_ip=False)
        self.assertEqual(0, mc.count)

        pium.is_ddns_outdated(update_current_ip=True)
        self.assertEqual(1, mc.count)

    def test_ddns_ip_initialization(self):
        # ddns_ip should be initialized with None value
        pium = DDNSManager(
            ip_getter=MockPublicIPGetter(get_current_ip_action=lambda: "whatever"),
            ddns_updater=MockDDNSUpdater(update_ddns_record_action=lambda ip: None),
        )
        self.assertIsNone(pium.ddns_ip)

    def test_ddns_ip_update_with_update_ip_false(self):
        # ddns_ip should be equal to #current_ip after #update_ddns without a update_current_ip
        test_ip = "test_ip"
        pium = DDNSManager(
            ip_getter=MockPublicIPGetter(get_current_ip_action=lambda: test_ip),
            ddns_updater=MockDDNSUpdater(update_ddns_record_action=lambda ip: None),
        )
        pium.update_ddns(update_current_ip=False)
        self.assertEqual(test_ip, pium.current_ip)
        self.assertEqual(test_ip, pium.ddns_ip)

    def test_ddns_ip_update_with_update_ip_true(self):
        # ddns_ip should be equal to #current_ip after #update_ddns with a update_current_ip
        test_ip = "test_ip"
        pium = DDNSManager(
            ip_getter=MockPublicIPGetter(get_current_ip_action=lambda: test_ip),
            ddns_updater=MockDDNSUpdater(update_ddns_record_action=lambda ip: None),
        )
        pium.update_ddns(update_current_ip=True)
        self.assertEqual(test_ip, pium.current_ip)
        self.assertEqual(test_ip, pium.ddns_ip)

    def test_ddns_ip_update_with_update_should_call_public_ip_getter(self):
        # ddns_ip with update_current_ip=True should call PublicIPGetter#get_current_ip()
        test_ip = "test_ip"
        mock_pig = MockPublicIPGetter(get_current_ip_action=lambda: test_ip)
        mock_du = MockDDNSUpdater(update_ddns_record_action=lambda ip: None)

        pium = DDNSManager(ip_getter=mock_pig, ddns_updater=mock_du)

        test_ip2 = "test_ip2"
        mc = CallRecorder(on_call=lambda: test_ip2)
        mock_pig.get_current_ip_action = mc
        self.assertEqual(0, mc.count)

        pium.update_ddns()

        self.assertEqual(1, mc.count)

    def test_ddns_ip_update_without_update_should_not_call_public_ip_getter(self):
        # ddns_ip with update_current_ip=True should call PublicIPGetter#get_current_ip()
        test_ip = "test_ip"
        mock_pig = MockPublicIPGetter(get_current_ip_action=lambda: test_ip)
        mock_du = MockDDNSUpdater(update_ddns_record_action=lambda ip: None)

        pium = DDNSManager(ip_getter=mock_pig, ddns_updater=mock_du)

        test_ip2 = "test_ip2"
        mc = CallRecorder(on_call=lambda: test_ip2)
        mock_pig.get_current_ip_action = mc
        self.assertEqual(0, mc.count)

        pium.update_ddns(update_current_ip=False)

        self.assertEqual(0, mc.count)

    def test_ddns_ip_update_should_call_ddns_updater(self):
        # update_ddns should call DDNSUpdater if ddns ip is not outdated
        mc = CallRecorder(on_call=lambda: None)
        mock_pig = MockPublicIPGetter(get_current_ip_action=lambda: "whatever")
        mock_du = MockDDNSUpdater(update_ddns_record_action=mc)

        pium = DDNSManager(ip_getter=mock_pig, ddns_updater=mock_du)
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
        mc = CallRecorder(on_call=lambda: None)
        mock_pig = MockPublicIPGetter(get_current_ip_action=lambda: "whatever")
        mock_du = MockDDNSUpdater(update_ddns_record_action=mc)

        pium = DDNSManager(ip_getter=mock_pig, ddns_updater=mock_du)
        self.assertEqual(0, mc.count)

        # ddns ip is outdated, DDNSUpdater is called
        self.assertNotEqual(pium.ddns_ip, pium.current_ip)
        pium.update_ddns(update_current_ip=False)
        self.assertEqual(1, mc.count)

        # ddns ip is not outdated, DDNSUpdater is not called
        self.assertEqual(pium.ddns_ip, pium.current_ip)
        pium.update_ddns(update_current_ip=True)
        self.assertEqual(1, mc.count)

    def test_loop_lifecycle(self):
        # loop should keep verifying if the the the public ip changed every X seconds and
        # if changed try to updated it in case of error  the error handler should be called
        # indefinitely, the loop only stops if the error handler fails

        # Scenario:
        #
        # Iteration cycle : 1s
        #
        # |         When          |    PublicIpGetter    |          DDNSUpdater           |         ErrorHandler         |
        # | :-------------------: | :------------------: | :----------------------------: | :--------------------------: |
        # | Manager instantiation |     () -> 'ip1'      |               -                |              -               |
        # |     Loop 1st pass     |     () -> 'ip1'      |        ('ip1') -> None         |              -               |
        # |     Loop 2nd pass     |     () -> 'ip1'      |               -                |              -               |
        # |     Loop 3rd pass     |     () -> 'ip2'      | ('ip2') -> Raise UpdateDDNSErr |   (UpdateDDNSErr) -> None    |
        # |     Loop 4th pass     |     () -> 'ip2'      |        ('ip2') -> None         |              -               |
        # |     Loop 5th pass     |     () -> 'ip2'      |               -                |              -               |
        # |     Loop 6th pass     | () -> raise GetIpErr |               -                | (GetIpErr) -> raise GetIpErr |
        #
        # Loops stops after 6th pass

        def ex(exception):
            def caller():
                raise exception

            return caller

        class GetIpErr(Exception):
            pass

        def get_current_ip_responses():
            yield lambda: "ip1"  # instantiation
            yield lambda: "ip1"  # 1st pass
            yield lambda: "ip1"  # 2nd pass
            yield lambda: "ip2"  # 3th pass
            yield lambda: "ip2"  # 4th pass
            yield lambda: "ip2"  # 5th pass
            yield ex(GetIpErr)  # 6th pass
            yield lambda: "wont hit"  # won't pass
            yield lambda: "wont hit"  # won't pass

        g = get_current_ip_responses()

        def get_current_ip_responder():
            return next(g)()

        get_current_ip_recorder = CallRecorder(on_call=get_current_ip_responder)
        mock_pig = MockPublicIPGetter(get_current_ip_action=get_current_ip_recorder)

        class UpdateDDNSErr(Exception):
            pass

        def update_ddns_record_responses():
            yield lambda: None  # 1st pass (first update)
            yield ex(UpdateDDNSErr)  # 3st pass
            yield lambda: None  # 4st pass (because the above pass failed)

        u = update_ddns_record_responses()

        def update_ddns_record_responder():
            return next(u)()

        update_ddns_record_recorder = CallRecorder(update_ddns_record_responder)
        mock_du = MockDDNSUpdater(update_ddns_record_action=update_ddns_record_recorder)

        class OnErrErr(Exception):
            pass

        def on_error_responses():
            yield lambda: None  # 3st pass
            yield ex(OnErrErr)  # 6st pass -> Loop stopped

        o = on_error_responses()

        def on_error_responder():
            return next(o)()

        on_error = CallRecorder(on_error_responder)

        pium = DDNSManager(ip_getter=mock_pig, ddns_updater=mock_du)

        # On instantiation nothing is 'touched'
        self.assertEqual(1, get_current_ip_recorder.count)
        self.assertEqual(0, update_ddns_record_recorder.count)
        self.assertEqual(0, on_error.count)

        interval = 1  # seconds

        # Loop should stop if on_error callable raises error
        self.assertRaises(
            OnErrErr, pium.update_loop, interval=interval, on_error=on_error
        )

        # Ip Getter is called 7 times
        self.assertEqual(7, get_current_ip_recorder.count)

        # The interval between each update try should be the one explicitly defined in the loop
        accepted_diff = timedelta(
            seconds=interval / 100
        )  # no particular reason for choosing 1% of interval as the maximum accepted error
        expected_interval = timedelta(seconds=interval)
        for index in range(
            2, len(get_current_ip_recorder.calls)
        ):  # 1st interval skipped (it' outside the loop)
            actual_interval = (
                get_current_ip_recorder.calls[index]["timestamp"]
                - get_current_ip_recorder.calls[index - 1]["timestamp"]
            )
            diff = abs(actual_interval - expected_interval)
            self.assertLess(diff, accepted_diff)

        # DDNS Updater is called 3 times
        self.assertEqual(3, update_ddns_record_recorder.count)
        #   1. Once for setting the ip = 'ip1'
        self.assertEqual(update_ddns_record_recorder.calls[0]["kwargs"]["ip"], "ip1")
        self.assertIsNone(update_ddns_record_recorder.calls[0]["response"])
        #   2. The second time when ip = 'ip2', but it fails
        self.assertEqual(update_ddns_record_recorder.calls[1]["kwargs"]["ip"], "ip2")
        self.assertIsInstance(
            update_ddns_record_recorder.calls[1]["exception"], UpdateDDNSErr
        )
        #   3. Since it fails it is called again
        self.assertEqual(update_ddns_record_recorder.calls[2]["kwargs"]["ip"], "ip2")
        self.assertIsNone(update_ddns_record_recorder.calls[2]["response"])

        # Error handler is called 2 times
        self.assertEqual(2, on_error.count)
        #   1. When update_ddns fails
        self.assertIsInstance(on_error.calls[0]["args"][0], UpdateDDNSErr)
        #   2. When get_ip fails
        self.assertIsInstance(on_error.calls[1]["args"][0], GetIpErr)
