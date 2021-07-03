from typing import Dict, Type

from ddns_manager.public_ip_getter import *
from .helpers import *


def public_ip_getter(config: Dict) -> PublicIPGetter:
    helper = factory(config.get("type"))
    pig = helper.build(config.get("details"))

    return pig


def factory(type_str: str) -> Type[PublicIpGetterConfigHelper]:
    selector = {"google": GoogleConfigHelper}
    if type_str not in selector:
        expected = selector.keys()
        expected_str = ", ".join(expected)
        raise AttributeError(
            f"Invalid public_ip_getter type (used: {type_str} / expected: [{expected_str}])"
        )

    return selector[type_str]
