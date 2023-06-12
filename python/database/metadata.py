"""
Contains all necessary information for each dataset scraped.
"""
from python.database.supported_file_type import SupportedFileType
from datetime import datetime


class Dataset:
    """
    Contains all relevant information for each dataset.
    """

    def __init__(self, title: str, languages: str | list, file_type: SupportedFileType, url: str, miscellaneous: list):
        """
        Params:
            title (str): The title of the dataset.
            languages (str|list): Any languages included in the dataset.
            file_type (str): The file type of the dataset.
            url (str): The URL to download the dataset.
            miscellaneous (list): Any miscellaneous information which may be relevant.
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

    def __init__(self, id: int, keywords: list, subjects: list, audience: list, start_date: str, end_date: str,
                 description: str, datasets: list):
        """
        Params:
            id (int): A unique identifier used to reference the MetaData.
            keywords (list): All keywords relating to the data.
            subjects (list): All potentially relevant subjects to the data.
            audience (list): The target demographic of the data.
            start_date (datetime): The beginning of the dataset's temporal coverage.
            end_date (datetime): The end of the dataset's temporal coverage.
            description (str): A string description of the dataset's contents.
            datasets (list(Database)): All datasets corresponding to the data.
        """

        self._id = id
        self._keywords = keywords
        self._subjects = subjects
        self._audience = audience
        self._start_date = start_date
        self._end_date = end_date
        self._description = description
        self._datasets = datasets

    @property
    def id(self) -> int:
        """
        Unique identifier used to reference the metadata.
        """
        return self._id

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
    def description(self) -> str:
        """
        Description of the data.
        """
        return self._description

    @property
    def datasets(self) -> list:
        """
        All datasets listed on the webpage.
        """
        return self._datasets
