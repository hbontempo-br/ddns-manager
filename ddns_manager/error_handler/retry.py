import logging
from .base import ErrorHandlerType


def retry_handler() -> ErrorHandlerType:
    return lambda e: logging.error(f"Error: {e}")
