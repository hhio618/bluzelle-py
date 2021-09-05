import logging

import colorlog


def get_logger(name: str, level: int) -> logging.Logger:
    """Create a (colored) logger with the given name.

    Args:
      name: logger specific name
      level: logging level
    """
    logger = logging.getLogger(name)

    if logger.hasHandlers() and len(logger.handlers) > 0:
        return logger

    formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(levelname)-8s%(reset)s %(white)s%(message)s",
        datefmt=None,
        reset=True,
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red,bg_white",
        },
        secondary_log_colors={},
        style="%",
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(level)

    return logger


def is_string(value):
    return isinstance(value, (str, bytes, bytearray))


def bytes_to_str(value):
    if isinstance(value, str):
        return value
    return value.decode("utf-8")
