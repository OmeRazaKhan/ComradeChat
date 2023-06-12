"""
Module providing a method of interacting with the data scraped from the open search portal.
"""
from python.database.parser import Parser
from python.database.metadata import Dataset, MetaData


class Database:

    def __init__(self, data_file_path: str):
        """
        Params:
            data_file_path(str): The file path to the JSON file containing the scraped web data.
        """
        self._data = Parser().parse()
        #data = list
        ids = [current_data.get_id() for current_data in data]
        ids_to_data = {
            ids: self._data
        }
        self._data.get_csv_url()

    @property
    def data(self) -> Data:
        """
        All data scraped from the web portal.
        """
        return self._data
