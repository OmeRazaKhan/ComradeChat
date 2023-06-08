
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

import python.scrapers.constants as constants


class Scraper:
    """
    Performs all scraping operations on the open source data portal.
    """

    def __init__(self, crawl_delay: float = constants.DEFAULT_CRAWL_DELAY):
        """
        Params:
            crawl_delay (int, default=DEFAULT_CRAWL_DELAY): The delay after loading a new webpage.
        """
        self._crawl_delay = crawl_delay

    @property
    def crawl_delay(self) -> float:
        """
        The time delay after loading a new webpage.
        """
        return self._crawl_delay

    def launch(self):
        """
        Launches the web scraper.
        """
        driver = webdriver.Firefox(
            executable_path=constants.SELENIUM_DRIVER_PATH)
