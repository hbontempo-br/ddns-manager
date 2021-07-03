from typing import Dict

from ddns_manager.cli.public_ip_getter.helpers.base import PublicIpGetterConfigHelper
from ddns_manager.public_ip_getter.google import GooglePublicIpGetter


class GoogleConfigHelper(PublicIpGetterConfigHelper):
    @classmethod
    def build(cls, config: Dict) -> GooglePublicIpGetter:
        return GooglePublicIpGetter()

    @staticmethod
    def new_config():
        return None
