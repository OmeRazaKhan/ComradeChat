"""
Module containing all configuration settings for selenium.
"""
from pathlib import Path

# Constants used for web scraping
SELENIUM_DRIVER_PATH = Path(
    "C:/DylanMunro/SeleniumDrivers/geckodriver.exe").absolute()
DEFAULT_CRAWL_DELAY = 5

# URL for the open data portal.
OPEN_DATA_PORTAL_URL = "https://search.open.canada.ca/opendata/?subject_en=Military&page=1&sort=metadata_modified+desc"
