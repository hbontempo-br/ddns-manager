import unittest

from tests.common import *
from ddns_domain_updater.ddns_updater import DDNSUpdater


class TestDDNSUpdater(unittest.TestCase):
    def test_get_current_ip_signature(self):
        # test if DDNSUpdater has the method update_ddns_record and if that has the correct signature
        method = get_method('update_ddns_record', DDNSUpdater)
        self.assertTrue(callable(method))
        self.assertTrue(is_abstract(method))
        # instance method -> arguments: [ip]
        self.assertEqual(('self', 'ip'), arguments(method))
