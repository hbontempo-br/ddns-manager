import logging

from ddns_manager import DDNSManager, GooglePublicIpGetter, GoogleSyntheticDDNSUpdater

from constants import *
from helper.logger import setup_console_logging

if __name__ == '__main__':

    # CONFIGURES LOGGER
    logger_format = "%(asctime)s | %(levelname)s - %(message)s"
    logger_date_time_format = "%Y-%m-%d %H:%M:%S"
    logger = setup_console_logging(logging.DEBUG, logger_format, logger_date_time_format)

    pig = GooglePublicIpGetter()
    du = GoogleSyntheticDDNSUpdater(
        username=USERNAME,
        password=PASSWORD,
        hostname=HOSTNAME
    )
    pium = DDNSManager(
        ip_getter=pig,
        ddns_updater=du
    )

    pium.update_loop(interval=UPDATE_DELAY)

