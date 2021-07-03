import unittest

from ddns_manager import GoogleSyntheticDDNSUpdater
from ddns_manager.cli.ddns_updater.base import factory, ddns_updater
from ddns_manager.cli.ddns_updater.helpers import GoogleSyntheticDDNSConfigHelper


class TestDDNSUpdaterCLI(unittest.TestCase):
    def test_factory_with_valid_type(self):
        cases = [("google_synthetic", GoogleSyntheticDDNSConfigHelper)]
        for ddns_type, expected_response in cases:
            self.assertIs(expected_response, factory(ddns_type))

    def test_factory_with_invalid_type(self):
        self.assertRaises(AttributeError, factory, "invalid type")

    def test_ddns_updater_with_valid_config(self):
        cases = [
            (
                {
                    "type": "google_synthetic",
                    "details": {
                        "username": "whatever",
                        "password": "whatever",
                        "hostname": "whatever",
                    },
                },
                GoogleSyntheticDDNSUpdater,
            )
        ]
        for config, expected_response in cases:
            self.assertIsInstance(ddns_updater(config), expected_response)
