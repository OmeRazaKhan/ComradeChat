
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

    def _get_button_number(self, button):
        """
        Returns the number embedded in a number to navigate to a different page in the Open Data Portal.

        Params:
            button: The WebElement version of the button.

        Returns:
            (int): The number on the button.
            (None): If no number could be found on the button.
        """
        button_html = button.text
        button_number_regex = "^(\d+)\D"
        button_string = re.findall(button_number_regex, button_html)[0]
        return int(button_string)

    def _get_num_search_pages(self, first_page_url: str) -> int:
        """
        Returns the total number of pages in the Open Data Portal.

        Params:
            first_page_url (str): The URL of the first search page results in the Open Data Portal.

        Returns:
            (int): The total number of webpages in the portal.

        Raises:
            Exception: If the button to the last page can not be located.
        """
        self._driver.get(constants.OPEN_DATA_PORTAL_URL)
        try:
            last_page_button = WebDriverWait(self._driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '/html/body/main/div[1]/div[3]/div[13]/div/ul/li[7]/a'))
            )
            number = self._get_button_number(last_page_button)
            return number
        except Exception as e:
            raise e

    def get_all_dataset_urls(self, max_urls: int = None) -> list:
        """
        Returns a list of all URLs in the Open Data Portal which lead to a dataset.

        Params:
            max_urls (int, default=None): The maximum amount of URLs to generate.
        """
        total_pages = self._get_num_search_pages(
            constants.OPEN_DATA_PORTAL_URL)
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
