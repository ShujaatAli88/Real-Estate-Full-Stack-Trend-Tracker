import os
import sys

from loguru import logger
from sentry_sdk.integrations.logging import ignore_logger

from scraper.constants import DATA_DIRECTORY, LOGS_FILE_NAME

class LogHandler:
    def __init__(self, logs_file_path: str) -> None:
        if os.path.exists(logs_file_path):
            os.remove(
                logs_file_path,
            )
        logger.remove()
        self.logs_file_path = logs_file_path
        self.logger = logger
        ignore_logger(self.logger.add(logs_file_path))
        ignore_logger(self.logger.add(sys.stderr, colorize=True))


LOGS_FILE_PATH = os.path.join(DATA_DIRECTORY, LOGS_FILE_NAME)

_logger = LogHandler(LOGS_FILE_PATH).logger

## example usage
# from log_handler import _logger
# _logger.info("Test Log")