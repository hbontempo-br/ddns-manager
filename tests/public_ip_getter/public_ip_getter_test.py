import unittest

from tests.common import *
from ddns_manager.public_ip_getter import PublicIPGetter


class TestPublicIpGetter(unittest.TestCase):
    def test_get_current_ip_signature(self):
        # test if PublicIPGetter has the method get_current_ip and if that has the correct signature

        # has should have method
        method = getattr(PublicIPGetter, "get_current_ip", None)
        self.assertTrue(callable(method))

        # check if is abstract
        self.assertTrue(is_abstract(method))

        # checks method signature
        self.assertEqual("(self) -> str", callable_signature(method))
