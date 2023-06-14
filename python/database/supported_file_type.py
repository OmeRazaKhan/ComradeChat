"""
All supported file types.
"""
from enum import Enum


class SupportedFileType(Enum):
    """
    All supported file types for datasets.
    """

    CSV = "csv"
    HTML = "html"
    JSON = "json"
    XLSX = "xlsx"
    XML = "xml"
