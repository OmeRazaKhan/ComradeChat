"""
Module containing all configuration settings for selenium.
"""
from pathlib import Path

# Constants used for web scraping
SELENIUM_DRIVER_PATH = Path(
    "C:/DylanMunro/SeleniumDrivers/geckodriver.exe").absolute()
DEFAULT_CRAWL_DELAY = 5
