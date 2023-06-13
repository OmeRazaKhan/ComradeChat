"""
Module containing all exceptions which may be thrown by the API.
"""


class NoResponseError(Exception):
    """
    Indicates that no response was generated for the given query.
    """

    def __init__(self, message: str):
        super().__init__(message)
