from typing import Dict, Type

from ddns_manager.ddns_updater import *
from .helpers import *


def ddns_updater(config: Dict) -> DDNSUpdater:
    helper = factory(config.get("type"))
    du = helper.build(config.get("details"))

    return du


def factory(type_str: str) -> Type[DDNSUpdaterConfigHelper]:
    selector = {"google_synthetic": GoogleSyntheticDDNSConfigHelper}
    if type_str not in selector:
        expected = selector.keys()
        expected_str = ", ".join(expected)
        raise AttributeError(
            f"Invalid ddns_updater type (used: {type_str} / expected: [{expected_str}])"
        )

    return selector[type_str]
