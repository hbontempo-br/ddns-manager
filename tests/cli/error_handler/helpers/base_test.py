import unittest

from tests.common import *
from ddns_manager.cli.error_handler.helpers.base import ErrorHandlerConfigHelper


class TestErrorHandlerConfigHelper(unittest.TestCase):
    def test_build_signature(self):
        # test if ErrorHandlerConfigHelper has the method build and if that has the correct signature

        # has should have method
        method = getattr(ErrorHandlerConfigHelper, "build", None)
        self.assertTrue(callable(method))

        # check if is abstract
        self.assertTrue(is_abstract(method))

        # checks method signature
        self.assertEqual(
            "(config: Dict) -> Callable[[Exception], NoneType]",
            callable_signature(method),
        )
