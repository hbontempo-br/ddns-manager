import unittest

from tests.common import *
from ddns_manager.cli.public_ip_getter.helpers.base import PublicIpGetterConfigHelper


class TestPublicIpGetterConfigHelper(unittest.TestCase):
    def test_build_signature(self):
        # test if PublicIpGetterConfigHelper has the method build and if that has the correct signature

        # has should have method
        method = getattr(PublicIpGetterConfigHelper, "build", None)
        self.assertTrue(callable(method))

        # check if is abstract
        self.assertTrue(is_abstract(method))

        # checks method signature
        self.assertEqual(
            "(config: Dict) -> ddns_manager.public_ip_getter.base.PublicIPGetter",
            callable_signature(method),
        )
