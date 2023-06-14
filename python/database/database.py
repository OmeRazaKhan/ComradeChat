"""
Module providing a method of interacting with the data scraped from the open search portal.
"""
from python.database.parser import Parser
from python.database.metadata import Dataset, MetaData


class Database:

    def __init__(self, ids_to_metadata: dict):
        self._ids_to_metadata = ids_to_metadata

    def get_all_descriptions(self) -> dict:
        """
        Returns:
            (dict(int: string)): The ID of each metadata entry mapped to the description of its dataset.
        """
        ids_to_descriptions = dict()
        for key in self._ids_to_metadata.keys():
            metadata = self._ids_to_metadata.get(key)
            description = metadata.description
            ids_to_descriptions[key] = description
        return ids_to_descriptions

    def get_metadata(self, key) -> dict:
        """
        Returns all metadata for the specified key.
        """
        return self._ids_to_metadata.get(key)

    def get_description(self, key) -> str:
        """
        Returns:
            (str): The description of the dataset referred to by the given key.
        """
        return self._ids_to_metadata.get(key).description

    def get_dataset_urls(self, key) -> str:
        """
        Returns:
            (str): The URL to the dataset referred to by the given key.
        """
        return self._ids_to_metadata.get(key).dataset.url

    def get_all_keys(self) -> list:
        """
        Returns:
            (list): All keys in the database.
        """
        return self._ids_to_metadata.keys()