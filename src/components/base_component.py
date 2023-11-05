import logging
from abc import ABC, abstractmethod
from typing import List, Union


class BaseComponent(ABC):
    """"""

    def __init__(self, logger_name):
        self.logger = self._configure_logger(logger_name)

    @staticmethod
    def _configure_logger(component_name):
        logger = logging.getLogger(component_name)
        logger.setLevel(logging.INFO)

        # Create a file handler for logging to a file
        file_handler = logging.FileHandler('logs.txt')
        file_handler.setLevel(logging.ERROR)

        # Create a formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        # Add the file handler to the logger
        logger.addHandler(file_handler)
        return logger


    def handle_error(self, error_message, exception=None):
        # Centralized error handling
        self.logger.error(error_message)
        if exception:
            self.logger.error(f"Exception: {str(exception)}")
        # You can add more error handling logic here, such as sending alerts or notifications

    def _run(self, input: Union[str, List[float]]) -> str:
        try:
            return self.run(input)
        except Exception as e:
            self.handle_error(f"An error occurred: {str(e)}", exception=e)
            return str(e)  # You can customize the return value in case of an error

    @abstractmethod
    def run(
            self,
            input: Union[str, List[float]],
    ) -> str:
        """Comment"""

    def run_async(
            self,
            input: Union[str, List[float]],
    ) -> str:
        """Comment"""
