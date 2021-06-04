from ddns_domain_updater.helper.environment import get_environment_variable

USERNAME = get_environment_variable("USERNAME")
PASSWORD = get_environment_variable("PASSWORD")
HOSTNAME = get_environment_variable("HOSTNAME")

UPDATE_DELAY = int(get_environment_variable("UPDATE_DELAY", 10))
