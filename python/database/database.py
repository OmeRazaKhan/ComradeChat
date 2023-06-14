"""
Module providing a method of interacting with the data scraped from the open search portal.
"""


class Database:

    def __init__(self, ids_to_metadata: dict):
        self._ids_to_metadata = ids_to_metadata

    def get_all_descriptions(self) -> dict:
        """
        Returns:
            (dict(int: string)): The ID of each metadata entry mapped to the description of its dataset.
        """
        ids_to_descriptions = dict()
        for id in self._ids_to_metadata.keys():
            metadata = self._ids_to_metadata.get(id)
            description = metadata.description
            ids_to_descriptions[id] = description
        return ids_to_descriptions

    def get_metadata(self, id: int) -> dict:
        """
        Returns:
            (dict): All metadata for the specified id.
        """
        return self._ids_to_metadata.get(id)

    def get_dataset_url(self, id: int) -> str:
        """
        Returns:
            (str): The URL for the dataset with the given id value.
        """
        return self._ids_to_metadata.get(id).dataset_url

    def get_description(self, id: int) -> str:
        """
        Returns:
            (str): The description of the dataset with the specified id.
        """
        return self._ids_to_metadata.get(id).description

    def get_resources(self, id: int) -> list:
        """
        Returns:
            (list): A list of all resources relevant to the dataset.
        """
        return self._ids_to_metadata.get(id).resources

    def get_all_keys(self):
        """
        Returns:
            (list): A list of all key values in the database.
        """
        return self._ids_to_metadata.keys()
