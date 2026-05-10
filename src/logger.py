import logging

from constants import BASE_LOGGER_NAME


def get_new_logger(module_path: str) -> logging.Logger:
    return logging.getLogger(f"{BASE_LOGGER_NAME}.{module_path}")
