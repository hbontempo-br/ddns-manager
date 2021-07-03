import unittest

from ddns_manager.cli.ddns_updater.helpers.google_synthetic_ddns import (
    GoogleSyntheticDDNSConfigHelper,
)
from ddns_manager.ddns_updater.google_synthetic import GoogleSyntheticDDNSUpdater


class TestGoogleSyntheticDDNSConfigHelper(unittest.TestCase):
    def test_check_config_with_valid_config(self):
        config = {
            "username": "whatever",
            "password": "whatever",
            "hostname": "whatever",
        }
        self.assertIsNone(GoogleSyntheticDDNSConfigHelper.check_config(config))

    def test_check_config_with_missing_key_config(self):
        config = {"password": "whatever", "hostname": "whatever"}
        self.assertRaises(
            AttributeError, GoogleSyntheticDDNSConfigHelper.check_config, config
        )

        config = {"username": "whatever", "hostname": "whatever"}
        self.assertRaises(
            AttributeError, GoogleSyntheticDDNSConfigHelper.check_config, config
        )

        config = {
            "username": "whatever",
            "password": "whatever",
        }
        self.assertRaises(
            AttributeError, GoogleSyntheticDDNSConfigHelper.check_config, config
        )

    def test_build_with_valid_config(self):
        config = {
            "username": "whatever",
            "password": "whatever",
            "hostname": "whatever",
        }
        du = GoogleSyntheticDDNSConfigHelper.build(config)
        self.assertIsInstance(du, GoogleSyntheticDDNSUpdater)
