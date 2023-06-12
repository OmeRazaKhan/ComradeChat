"""
Module providing a method of interacting with the data scraped from the open search portal.
"""
from python.database.parser import Parser
from python.database.dataset import Data, Dataset


class Database:

    def __init__(self, data_file_path: str):
        """
        Params:
            data_file_path(str): The file path to the JSON file containing the scraped web data.
        """
        self._data = Parser().parse()

    @property
    def data(self) -> Data:
        """
        All data scraped from the web portal.
        """
        return self._data
