import unittest

from tests.common import *
from ddns_domain_updater.public_ip_getter import PublicIPGetter


class TestPublicIpGetter(unittest.TestCase):
    def test_get_current_ip_signature(self):
        # test if PublicIPGetter has the method get_current_ip and if that has the correct signature
        method = get_method('get_current_ip', PublicIPGetter)
        self.assertTrue(callable(method))
        self.assertTrue(is_abstract(method))
        # instance method -> arguments: []
        self.assertEqual(('self',), arguments(method))
