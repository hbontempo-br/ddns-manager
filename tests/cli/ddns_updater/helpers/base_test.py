import unittest

from tests.common import *
from ddns_manager.cli.ddns_updater.helpers.base import DDNSUpdaterConfigHelper


class TestDDNSUpdaterConfigHelper(unittest.TestCase):
    def test_build_signature(self):
        # test if DDNSUpdaterConfigHelper has the method build and if that has the correct signature

        # has should have method
        method = getattr(DDNSUpdaterConfigHelper, "build", None)
        self.assertTrue(callable(method))

        # check if is abstract
        self.assertTrue(is_abstract(method))

        # checks method signature
        self.assertEqual(
            "(config: Dict) -> ddns_manager.ddns_updater.base.DDNSUpdater",
            callable_signature(method),
        )
