from typing import Dict

from ddns_manager.ddns_updater.google_synthetic import GoogleSyntheticDDNSUpdater
from .base import DDNSUpdaterConfigHelper


class GoogleSyntheticDDNSConfigHelper(DDNSUpdaterConfigHelper):
    @classmethod
    def build(cls, config: Dict) -> GoogleSyntheticDDNSUpdater:
        cls.check_config(config=config)
        return GoogleSyntheticDDNSUpdater(
            username=config["username"],
            password=config["password"],
            hostname=config["hostname"],
        )

    @staticmethod
    def new_config():
        # TODO: implement interactive CLI to help generating the configuration
        raise NotImplementedError

    @classmethod
    def check_config(cls, config: Dict):
        # No need to get worried about different config versions for now
        # version = config.get('version', '0.1.0')

        required_keys = ["username", "password", "hostname"]

        for key in required_keys:
            if key not in config:
                raise AttributeError(
                    f"Invalid ddns_updater configuration file. (Missing '{key}' value)"
                )
