
import time
import re
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
        self._driver = None

    @property
    def crawl_delay(self) -> float:
        """
        The time delay after loading a new webpage.
        """
        return self._crawl_delay

    def _is_dataset_url(self, url: str) -> bool:
        """
        Returns:
            (bool) True if the URL contains a dataset, False otherwise.
        """
        # Regex to match a URL containing a dataset.
        dataset_regex = "^(https:\/\/open\.canada\.ca\/data\/.+\/dataset\/.+)$"
        if not re.match(dataset_regex, url) is None:
            return True
        return False

    def get_all_dataset_urls(self, max_urls: int = None) -> list:
        """
        Returns a list of all URLs in the Open Data Portal which lead to a dataset.

        Params:
            max_urls (int, default=None): The maximum amount of URLs to generate.
        """

        self._driver.get(constants.OPEN_DATA_PORTAL_URL)
        try:
            root_div = WebDriverWait(self._driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '/html/body/main/div[1]/div[3]'))
            )
        except Exception as e:
            print("Element not found")
            print(str(e))

        anchors = root_div.find_elements(by=By.XPATH, value=".//a")
        urls = [anchor.get_attribute('href') for anchor in anchors]
        dataset_urls = []
        for url in urls:
            if self._is_dataset_url(url):
                dataset_urls.append(url)
        print(dataset_urls)

    def launch(self):
        """
        Launches the web scraper.
        """
        self._driver = webdriver.Firefox(
            executable_path=constants.SELENIUM_DRIVER_PATH)
