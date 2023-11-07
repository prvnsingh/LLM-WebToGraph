import logging
from abc import ABC, abstractmethod
from functools import wraps
from typing import List, Union


def log_errors(logger):
    def decorator(run):
        @wraps(run)
        def wrapper(*args, **kwargs):
            try:
                return run(*args, **kwargs)
            except Exception as e:
                logger.log_error(f"An error occurred: {str(e)}", exception=e)

        return wrapper

    return decorator


class BaseComponent(ABC):
    """"""

    def __init__(self, logger_name):
        self.logger = self._configure_logger(logger_name)

    @log_errors
    @abstractmethod
    def run(
            self,
            input: Union[str, List[float]],
    ) -> str:
        """Comment"""

    @log_errors
    async def run_async(
            self,
            input: Union[str, List[float]],
    ) -> str:
        """Comment"""

    @staticmethod
    def _configure_logger(component_name):
        logger = logging.getLogger(component_name)
        logger.setLevel(logging.INFO)

        # Create a file handler for logging to a file
        file_handler = logging.FileHandler('logs/logs.txt')

        # Create a formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        # Add the file handler to the logger
        logger.addHandler(file_handler)
        return logger

    def log_error(self, error_message, exception=None):
        # Centralized error handling
        self.logger.error(error_message)
        if exception:
            self.logger.error(f"Exception: {str(exception)}")
        # You can add more error handling logic here, such as sending alerts or notifications
