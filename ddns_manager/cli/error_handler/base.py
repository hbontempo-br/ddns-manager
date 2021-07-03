from typing import Dict, Type

from ddns_manager.error_handler import *
from .helpers import *


def error_handler(config: Dict) -> ErrorHandlerType:
    helper = factory(config.get("type"))
    eh = helper.build(config.get("details"))

    return eh


def factory(type_str: str) -> Type[ErrorHandlerType]:
    selector = {"retry": RetryConfigHelper}
    if type_str not in selector:
        expected = selector.keys()
        expected_str = ", ".join(expected)
        raise AttributeError(
            f"Invalid on_error_behaviour type (used: {type_str} / expected: [{expected_str}])"
        )

    return selector[type_str]
