import logging
import time

from requests import get, Response
from retry import retry

from constants import *
from src.configuration.logger import setup_console_logging

# CONFIGURES LOGGER
logger_format = "%(asctime)s | %(levelname)s - %(message)s"
logger_date_time_format = "%Y-%m-%d %H:%M:%S"
logger = setup_console_logging(logging.DEBUG, logger_format, logger_date_time_format)


@retry(tries=3, delay=2)
def update_routine(username: str, password: str, hostname: str, ip: str):
    """
    Updates Google Domains Synthetic Records wit the provided IP.

    :param username: Synthetic Record username
    :param password: Synthetic Record password
    :param hostname: Synthetic Record hostname
    :param ip: current IP address
    :return: None
    """

    def validate_google_response(response: Response):
        """
        Validates Synthetic Record update request response validation
        :param response: alidates Synthetic Record update request response
        :return: None
        """
        response.raise_for_status()
        if not ("good" in response.text or "nochg" in response.text):
            raise Exception(f"Bad response: {response.text}")

    new_ip = get('https://api.ipify.org').text
    if new_ip == ip:
        logger.info(f"Current address is up to date, nothing to do ({new_ip}).")
        return ip

    try:
        logger.info(
            f"Current address is out of date, changing from {ip} to {new_ip}..."
        )
        url = f"https://{username}:{password}@domains.google.com/nic/update?hostname={hostname}&myip={new_ip}"
        response = get(url)
        validate_google_response(response=response)

        logger.info("Current address is now up to date.")
        return new_ip
    except Exception as ex:
        logger.error(f"Can't update current address due to an error ({ex})!")


ip = ""
logger.debug("Starting application")
while True:
    ip = update_routine(username=USERNAME, password=PASSWORD, hostname=HOSTNAME, ip=ip)
    logger.debug(f"Sleeping: {UPDATE_DELAY}")
    time.sleep(UPDATE_DELAY)
