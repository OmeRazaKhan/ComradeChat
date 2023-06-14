import time
import re
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

import python.scrapers.config as config
from python.scrapers.scraper import Scraper


class UrlScraper(Scraper):
    """
    Performs all scraping operations on the open source data portal.
    """

    def __init__(self, crawl_delay: float = config.DEFAULT_CRAWL_DELAY):
        """
        Params:
            crawl_delay (int, default=DEFAULT_CRAWL_DELAY): The delay after loading a new webpage.
        """
        super().__init__(crawl_delay=crawl_delay)

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
        self._driver.get(first_page_url)
        time.sleep(self.crawl_delay)
        try:
            last_page_button = WebDriverWait(self._driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "/html/body/main/div[1]/div[3]/div[13]/div/ul/li[7]/a")
                )
            )
            number = self._get_button_number(last_page_button)
            return number
        except Exception as e:
            raise e

    def _generate_all_search_portal_urls(
        self, first_page_url: str, total_pages: int
    ) -> list:
        """
        Generates the URL to all search index URLs on the open data portal.

        Params:
            first_page_url (str): The URL to the first page of the open data portal.
            total_pages (int): The total number of pages in the search portal.

        Returns:
            list(str): The URL to every search page of the open data portal.
        """
        # Locates the page number in a URL of the Open Data Portal's search section.
        page_number_regex = "(?<=&page=)\d+(?=&)"
        all_urls = []
        for i in range(1, total_pages + 1):
            url = re.sub(page_number_regex, str(i), first_page_url)
            all_urls.append(url)
        return all_urls

    def get_all_dataset_urls(self, first_page_url: str, max_urls: int = None) -> list:
        """
        Returns a list of all URLs in the Open Data Portal which lead to a dataset.

        Params:
            first_page_url (str): The URL to the first page of the Open Search Portal.
            max_urls (int, default=None): The maximum amount of URLs to generate.

        Returns:
            (list): The list of all URLs leading to a dataset on the Open Portal.
        """
        self._driver = webdriver.Firefox(executable_path=config.SELENIUM_DRIVER_PATH)

        # Obtain the URLs to all main pages in the search portal.
        total_pages = self._get_num_search_pages(first_page_url)
        search_portal_urls = self._generate_all_search_portal_urls(
            first_page_url, total_pages
        )

        all_dataset_urls = []

        total_dataset_urls_generated = 0
        for search_portal_url in search_portal_urls:
            self._driver.get(search_portal_url)
            time.sleep(self.crawl_delay)
            try:
                root_div = WebDriverWait(self._driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "/html/body/main/div[1]/div[3]")
                    )
                )
            except Exception as e:
                print("Element not found")
                print(str(e))

            anchors = root_div.find_elements(by=By.XPATH, value=".//a")
            urls = [anchor.get_attribute("href") for anchor in anchors]
            for url in urls:
                if self._is_dataset_url(url):
                    all_dataset_urls.append(url)
                    total_dataset_urls_generated += 1
                    if (
                        not max_urls is None
                        and total_dataset_urls_generated == max_urls
                    ):
                        break

            if not max_urls is None and total_dataset_urls_generated == max_urls:
                break

        self._driver.close()
        return all_dataset_urls
