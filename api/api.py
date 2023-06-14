from python.database.parser import Parser
from python.database.database import Database
from milvus_db.setup_database import setup_db
from milvus_db.predict import search
from api.exceptions import NoResponseError
from api.response import Response

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
        setup_db(ids_to_descriptions)

    def _create_response(self, relevant_response_ids: list) -> json:
        """
        Creates a JSON response from the list of id matches.

        Params:
            relevant_response_ids(list(int)): The most relevant responses to the query.
                This must be sorted such that the first element in the list is the most relevant response, and the last element in the list is more irrelevant.

        Returns:
            (json): The JSON response to the query.
        """
        rankings = [i for i in range(1, len(relevant_response_ids) + 1)]
        dataset_urls = [self._db.get_dataset_url(id) for id in relevant_response_ids]
        dataset_descriptions = [
            self._db.get_description(id) for id in relevant_response_ids
        ]
        resources = [self._db.get_resources(id) for id in relevant_response_ids]

        responses = []
        for i in range(len(relevant_response_ids)):
            response = Response(
                relevant_response_ids[i],
                rankings[i],
                dataset_urls[i],
                dataset_descriptions[i],
                resources[i],
            )
            responses.append(response.to_dict())
        json_response = json.dumps(responses)
        json_response = json.loads(json_response)
        return json_response

    def generate_response(self, query: str, maximum_num_responses: int = 3) -> json:
        """
        Generates a response to the user query.

        Params:
            query (str): The user's query.
            maximum_num_responses (int, default=3): The maximum number of responses that should be returned from the chatbot.

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
                        "dataset_description": "The description of the most relevant dataset to the user's query",
                        "message": "A message outputted by the backend describing any information to the user if needed",
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
                        "dataset_description": "The description of the most relevant dataset to the user's query",
                        "message": "A message outputted by the backend describing any information to the user if needed",
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

        ids = search(query)
        # ids = [2, 1]  # 1 is the most relevant, followed by
        if ids is None or len(ids) == 0:
            raise NoResponseError(
                "The query {} did not generate any responses".format(query)
            )

        response = self._create_response(ids)
        return response
