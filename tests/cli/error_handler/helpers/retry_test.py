import unittest

from ddns_manager.cli.error_handler.helpers.retry import RetryConfigHelper
from ddns_manager.error_handler.retry import retry_handler


class TestRetryConfigHelper(unittest.TestCase):
    def test_build_with_valid_config(self):
        config = {}
        eh = RetryConfigHelper.build(config)
        self.assertEqual(eh.__code__, retry_handler().__code__)

    def test_new_config(self):
        actual = RetryConfigHelper.new_config()
        self.assertIsNone(actual)
