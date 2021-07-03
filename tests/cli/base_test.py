import unittest
from ddns_manager.cli.base import check_config


class TestBaseCLI(unittest.TestCase):
    def test_check_config_with_valid_config(self):
        config = {
            "public_ip_getter": "whatever",
            "ddns_updater": "whatever",
            "check_interval": 1,
            "on_error_behaviour": "whatever",
        }
        self.assertIsNone(check_config(config))

    def test_check_config_with_missing_key_config(self):
        config = {
            "ddns_updater": "whatever",
            "check_interval": 1,
            "on_error_behaviour": "whatever",
        }
        self.assertRaises(AttributeError, check_config, config)

        config = {
            "public_ip_getter": "whatever",
            "check_interval": 1,
            "on_error_behaviour": "whatever",
        }
        self.assertRaises(AttributeError, check_config, config)

        config = {
            "public_ip_getter": "whatever",
            "ddns_updater": "whatever",
            "on_error_behaviour": "whatever",
        }
        self.assertRaises(AttributeError, check_config, config)

        config = {
            "public_ip_getter": "whatever",
            "ddns_updater": "whatever",
            "check_interval": 1,
        }
        self.assertRaises(AttributeError, check_config, config)

    def test_check_config_with_check_interval_not_integer(self):
        config = {
            "public_ip_getter": "whatever",
            "ddns_updater": "whatever",
            "check_interval": "not an integer",
            "on_error_behaviour": "whatever",
        }
        self.assertRaises(AttributeError, check_config, config)

    # TODO: Add tests to function 'loop'
