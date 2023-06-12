"""
Contains all necessary information for each dataset scraped.
"""
from python.parsers.supported_file_type import SupportedFileType


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


class Tags:

    def __init__(self, keywords: list, subjects: list, audience: list, start: str, end: str,
                 description: str, datasets: list | Dataset)
