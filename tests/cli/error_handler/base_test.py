import unittest

from ddns_manager import retry_handler
from ddns_manager.cli.error_handler.base import factory, error_handler
from ddns_manager.cli.error_handler.helpers import RetryConfigHelper


class TestErrorHandlerCLI(unittest.TestCase):
    def test_factory_with_valid_type(self):
        cases = [("retry", RetryConfigHelper)]
        for ddns_type, expected_response in cases:
            self.assertIs(expected_response, factory(ddns_type))

    def test_factory_with_invalid_type(self):
        self.assertRaises(AttributeError, factory, "invalid type")

    def test_error_handler_with_valid_config(self):
        cases = [
            ({"type": "retry", "details": None}, retry_handler()),
            ({"type": "retry", "details": {}}, retry_handler()),
            ({"type": "retry"}, retry_handler()),
        ]
        for config, expected_response in cases:
            self.assertEqual(error_handler(config).__code__, expected_response.__code__)
