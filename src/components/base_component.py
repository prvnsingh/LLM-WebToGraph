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
