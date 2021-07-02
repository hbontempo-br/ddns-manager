import unittest

from ddns_manager.cli.public_ip_getter.helpers.google import GoogleConfigHelper
from ddns_manager.public_ip_getter.google import GooglePublicIpGetter


class TestGoogleConfigHelper(unittest.TestCase):
    def test_build_with_valid_config(self):
        config = {}
        pig = GoogleConfigHelper.build(config)
        self.assertIsInstance(pig, GooglePublicIpGetter)

    def test_new_config(self):
        actual = GoogleConfigHelper.new_config()
        self.assertIsNone(actual)
