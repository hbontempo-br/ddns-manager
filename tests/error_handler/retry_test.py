import unittest

from tests.common import callable_signature
from ddns_manager.error_handler import retry_handler


class TestRetryHandler(unittest.TestCase):
    def test_retry_handler_signature(self):
        expected = "() -> Callable[[Exception], NoneType]"
        actual = callable_signature(retry_handler)
        self.assertEqual(expected, actual)

        expected = "(e)"  # lambda e
        actual = callable_signature(retry_handler())
        self.assertEqual(expected, actual)

    def test_handler_just_logs_error(self):
        with self.assertLogs(level="INFO") as cm:
            retry_handler()(Exception("Any error"))
        self.assertEqual(cm.output, ["ERROR:root:Error: Any error"])
