"""
Script to parse scraped metadata from a JSON file into a database.
"""

from python.database.parser import Parser


def parse_metadata(metadata_file_path: str) -> dict:
    """
    Parses the metadata for each entry in the JSON file.

    Params:
        metadata_file_path (str): The path to the JSON file containing all metadata for the scraped websites.

    Returns:
        (dict(MetaData)): The id of each metadata entry mapped to the metadata itself
    """
    parser = Parser()
    all_metadata = parser.parse(metadata_file_path)
    return all_metadata
