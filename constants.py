import os

USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")
HOSTNAME = os.environ.get("HOSTNAME")

UPDATE_DELAY = int(os.environ.get("UPDATE_DELAY", 10))
