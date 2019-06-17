import time
import logging

from ipify import get_ip
from requests import get, Response
from retry import retry

from constants import *

from src.helper.environment import get_environment_variable

logging.basicConfig(level=logging.DEBUG)


def validate_google_response(response: Response):
    response.raise_for_status()
    if not ("good" in response.text or "nochg" in response.text):
        raise Exception(f"Bad response: {response.text}")


@retry(tries=3, delay=2)
def update_routine(username: str, password: str, hostname: str, ip: str):
    new_ip = get_ip()
    logging.debug(f"External IP: {new_ip}")
    if new_ip != ip:
        url = f"https://{username}:{password}@domains.google.com/nic/update?hostname={hostname}&myip={new_ip}"
        response = get(url)
        validate_google_response(response=response)
        logging.debug(f"Record updated: {ip} > {new_ip}")
        return new_ip
    return ip


ip = ""
logging.debug("Starting application")
while True:
    ip = update_routine(username=USERNAME, password=PASSWORD, hostname=HOSTNAME, ip=ip)
    logging.debug(f"Sleeping: {UPDATE_DELAY}")
    time.sleep(UPDATE_DELAY)
