import unittest
from typing import NoReturn

from tests.common import *
from ddns_manager.ddns_updater import DDNSUpdater


class TestDDNSUpdater(unittest.TestCase):
    def test_get_current_ip_signature(self):
        # test if DDNSUpdater has the method update_ddns_record and if that has the correct signature

        # has should have method
        method = getattr(DDNSUpdater, "update_ddns_record", None)
        self.assertTrue(callable(method))

        # check if is abstract
        self.assertTrue(is_abstract(method))

        # checks method signature
        self.assertEqual("(self, ip: str) -> NoReturn", callable_signature(method))
