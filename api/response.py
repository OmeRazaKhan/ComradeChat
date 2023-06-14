"""
Module containing the Response object returned in response to a query.
"""


class Response:
    """
    Contains all relevant information to a user's query.
    """

    def __init__(
        self,
        id: int,
        ranking: int,
        dataset_url: str,
        dataset_description: str,
        resources: list,
        message: str = None,
    ):
        """
        Params:
            id (int): The id
        """
        self._id = id
        self._ranking = ranking
        self._dataset_url = dataset_url
        self._dataset_description = dataset_description
        self._resources = resources
        if message is None:
            self._message = "The following datasets may be relevant to your query."
        else:
            self._message = message

    def to_dict(self) -> dict:
        response_dict = dict()
        response_dict["id"] = self._id
        response_dict["dataset_url"] = self._dataset_url
        response_dict["dataset_description"] = self._dataset_description
        response_dict["message"] = self._message
        if not self._resources is None:
            all_resources = []
            for resource in self._resources:
                all_resources.append(str(resource))
            response_dict["resources"] = all_resources
        return response_dict
