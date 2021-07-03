import unittest

from ddns_manager import GooglePublicIpGetter
from ddns_manager.cli.public_ip_getter.base import factory, public_ip_getter
from ddns_manager.cli.public_ip_getter.helpers import GoogleConfigHelper


class TestPublicIpGetterCLI(unittest.TestCase):
    def test_factory_with_valid_type(self):
        cases = [("google", GoogleConfigHelper)]
        for ddns_type, expected_response in cases:
            self.assertIs(expected_response, factory(ddns_type))

    def test_factory_with_invalid_type(self):
        self.assertRaises(AttributeError, factory, "invalid type")

    def test_public_ip_getter_with_valid_config(self):
        cases = [
            ({"type": "google", "details": None}, GooglePublicIpGetter),
            ({"type": "google", "details": {}}, GooglePublicIpGetter),
            ({"type": "google"}, GooglePublicIpGetter),
        ]
        for config, expected_response in cases:
            self.assertIsInstance(public_ip_getter(config), expected_response)
