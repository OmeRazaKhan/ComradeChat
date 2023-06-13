from python.database.parser import Parser
from python.database.database import Database
#from milvus_db.setup_database import setup_db
#from milvus_db.predict import search
from api.exceptions import NoResponseError

import json


class API:
    """
    Interface for interacting with the program backend.
    """

    def __init__(self, json_dataset_file_path: str):
        parser = Parser()
        all_metadata = parser.parse(json_dataset_file_path)
        self._db = Database(all_metadata)
        ids_to_descriptions = self._db.get_all_descriptions()
        # setup_db(ids_to_descriptions)

    def generate_response(self, query: str, maximum_num_responses: int = 3, throw_no_response_error: bool = False) -> json:
        """
        Generates a response to the user query.

        Params:
            query (str): The user's query.
            maximum_num_responses (int, default=3): The maximum number of responses that should be returned from the chatbot.
            throw_no_response_error (bool, default=False): Temporary variable to test handling no response errors.
                If this is set to True, this function will raise a NoResponseError.

        Raises:
            NoResponseError: If the query did not generate a response from the chatbot.

        Returns:
            (json): JSON response to the query.
                A response will be in a similar format to the following:
                    [
                        {
                            "ranking": 1,
                            "dataset_id": 31,
                            "dataset_url": "https://open.canada.ca/data/en/dataset/3ac0d080-6149-499a-8b06-7ce5f00ec56c",
                            "description": "The description of the most relevant dataset to the user's query",
                            "resources": [
                                {
                                    "title": "Resource 1 title",
                                    "download_url": "https://open.canada.ca/data/dataset/id_31_dataset_1.csv",
                                    "data_format": "csv",
                                    "languages": [
                                        "en",
                                        "fr"
                                    ]
                                },
                                {
                                    "title": "Resource 2 title",
                                    "download_url": "https://open.canada.ca/data/dataset/id_31_dataset_2.json",
                                    "data_format": "json",
                                    "languages": [
                                        "en"
                                    ]
                                }
                            ]
                        },
                        {
                            "ranking": 2,
                            "dataset_id": 7,
                            "dataset_url": "https://open.canada.ca/data/en/dataset/e33bcd95-d0e5-4ade-9f5c-78f0a5a4d7a0",
                            "description": "The description of the most relevant dataset to the user's query",
                            "resources": [
                                {
                                    "title": "Resource 1 title",
                                    "download_url": "https://open.canada.ca/data/dataset/id_7_dataset_1.csv",
                                    "data_format": "csv",
                                    "languages": [
                                        "fr"
                                    ]
                                }
                            ]
                        }
                    ]
        """
        if throw_no_response_error:
            raise NoResponseError("Placeholder text for NoResponseError")

        # ids = search("Insert query here")
        ids = [1, 6, 3]  # 1 is the most relevant, followed by

        with open("resources/sample_response.json", "r", encoding="utf-8") as f:
            sample_response = json.load(f)
        return sample_response
