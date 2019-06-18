import logging


CONSOLE_LOGGER="console"
FILE_LOGGER="file"


def setup_console_logging(level, formatter, date_time_format):
    """
    Configures setup logging.

    :param level: Log level.
    :param formatter: Log message formatter.

    :returns: A console logger with the specified configuration.
    """
    logger = logging.getLogger(CONSOLE_LOGGER)
    logger.setLevel(level)

    formatter = logging.Formatter(formatter, date_time_format)

    handler = logging.StreamHandler()
    handler.setLevel(level)
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger


def setup_file_logging(level, formatter, date_time_format, path):
    """
    Configures setup logging.

    :param level: Log level.
    :param formatter: Log message formatter.
    :param path: Log file path.

    :returns: A file logger with the specified configuration.
    """
    logger = logging.getLogger(FILE_LOGGER)
    logger.setLevel(level)

    formatter = logging.Formatter(formatter, date_time_format)

    handler = logging.FileHandler(path)
    handler.setLevel(level)
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger
