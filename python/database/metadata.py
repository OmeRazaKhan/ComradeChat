"""
Contains all necessary information for each dataset scraped.
"""
from python.database.supported_file_type import SupportedFileType
from datetime import datetime
from typing import Any


class Resource:
    """
    Contains all relevant information for each dataset.
    """

    def __init__(self, title: str = None, languages: list = None, file_type: str = None, url: str = None, miscellaneous: list = None):
        """
        Params:
            title (str, default=None): The title of the dataset.
            languages (list, default=None): Any languages included in the dataset.
            file_type (SupportedFileType, default=None): The file type of the dataset.
            url (str, default=None): The URL to download the dataset.
            miscellaneous (list, default=None): Any miscellaneous information which may be relevant.
        """
        self._title = title
        if type(languages) is str:
            languages = [languages]
        self._languages = languages
        self._file_type = file_type
        self._url = url
        self._miscellaneous = miscellaneous

    @property
    def title(self) -> str:
        """
        The title given to the dataset.
        """
        return self._title

    @property
    def languages(self) -> list:
        """
        All languages used in the dataset.
        """
        return self._languages

    @property
    def file_type(self) -> SupportedFileType:
        """
        The file type of the dataset.
        """
        return self._file_type

    @property
    def miscellaneous(self) -> list:
        """
        Miscellaneous data which may be useful.
        """
        return self._miscellaneous


class MetaData:
    """
    Contains all metadata for each website scraped.
    """

    def __init__(self, id: int, description: str, dataset_url: str, keywords: list = None, subjects: list = None,
                 audience: list = None, start_date: datetime = None, end_date: datetime = None, resources: list = None):
        """
        Params:
            id (int): A unique identifier used to reference the MetaData.
            description (str): A description of the information presented by the dataset.
            dataset_url (str): The URL of the dataset.
            keywords (list, default=None): All keywords relating to the data.
            subjects (list, default=None): All potentially relevant subjects to the data.
            audience (list, default=None): The target demographic of the data.
            start_date (datetime, default=None): The beginning of the dataset's temporal coverage.
            end_date (datetime, default=None): The end of the dataset's temporal coverage.
            resources (list(Resource), default=None): All resources listed in the dataset.
        """

        self._id = id
        self._description = description
        self._dataset_url = dataset_url

        self._keywords = keywords
        self._subjects = subjects
        self._audience = audience
        self._start_date = start_date
        self._end_date = end_date
        self._resources = resources

    @property
    def id(self) -> int:
        """
        Unique identifier used to reference the metadata.
        """
        return self._id

    @property
    def description(self) -> str:
        """
        Description of the data.
        """
        return self._description

    @property
    def dataset_url(self) -> str:
        """
        The dataset's URL.
        """
        return self._dataset_url

    @property
    def keywords(self) -> list:
        """
        All keywords pertaining to the data.
        """
        return self._keywords

    @property
    def subjects(self) -> list:
        """
        All potentially relevant subjects to the data.
        """
        return self._subjects

    @property
    def audience(self) -> list:
        """
        The target demographics of the data.
        """
        return self._audience

    @property
    def start_date(self) -> datetime:
        """
        The beginning of the dataset's temporal coverage.
        """
        return self._start_date

    @property
    def end_date(self) -> datetime:
        """
        The end of the dataset's temporal coverage.
        """
        return self._end_date

    @property
    def resources(self) -> list:
        """
        All resources listed in the dataset.
        """
        return self._resources
