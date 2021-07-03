import unittest

from tests.common import *
from ddns_manager.cli.helpers import ConfigHelper


class TestConfigHelper(unittest.TestCase):
    def test_build_signature(self):
        # test if ConfigHelper has the method build and if that has the correct signature

        # has should have method
        method = getattr(ConfigHelper, "build", None)
        self.assertTrue(callable(method))

        # check if is abstract
        self.assertTrue(is_abstract(method))

        # checks method signature
        self.assertEqual("(config: Dict) -> object", callable_signature(method))

    def test_new_config_signature(self):
        # test if ConfigHelper has the method new_config and if that has the correct signature

        # has should have method
        method = getattr(ConfigHelper, "new_config", None)
        self.assertTrue(callable(method))

        # check if is abstract
        self.assertTrue(is_abstract(method))

        # checks method signature
        self.assertEqual("() -> Dict", callable_signature(method))
