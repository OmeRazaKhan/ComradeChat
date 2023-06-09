
import time
import re
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

import python.scrapers.config as config
from python.scrapers.scraper import Scraper


class DataScraper(Scraper):
    """
    Scrapes all relevant information from a URL containing a dataset.
    """

    def __init__(self, dataset_url: str, crawl_delay: float = config.DEFAULT_CRAWL_DELAY):
        """
        Params:
            dataset_url(str): The URL of the dataset.
            crawl_delay (int, default=DEFAULT_CRAWL_DELAY): The delay after loading a new webpage.
        """
        self._dataset_url = dataset_url
        super().__init__(crawl_delay=crawl_delay)

    @property
    def dataset_url(self) -> str:
        """
        The URL of the dataset.
        """
        return self._dataset_url

    def _strip_html_tags(self, text: str) -> str:
        """
        Removes all HTML tags from a string.
            For example, <p>Hello World</p> will return "Hello World".

        Params:
            text (str): The text to be stripped.

        Returns:
            (str): The text without any HTML tags.
        """
        html_regex = "<[^>]+>"
        return re.sub(html_regex, "", text)

    def _get_keywords(self) -> list:
        """
        Returns a list of all keywords about the dataset on a webpage.

        Raises:
            Warning: If the section could not be identified to have keywords.
            Exception: If an element could not be located.
        """
        try:
            keywords_div = WebDriverWait(self._driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div/div/main/div[2]/aside/div[2]/ul/li[2]"))
            )
            keyword_title_path = keywords_div.find_element(
                by=By.XPATH, value="./strong")
            if not "Keyword" in keyword_title_path.text:
                raise Warning("Did not find keyword section")
            keywords = []
            keywords_ul = keywords_div.find_element(by=By.XPATH, value="./ul")
            WebDriverWait(keywords_ul, 10).until(
                EC.presence_of_element_located((By.XPATH, './*')))
            keywords_li = keywords_ul.find_elements(by=By.XPATH, value="./*")
            for keyword_li in keywords_li:
                keyword_text = keyword_li.text
                keyword = self._strip_html_tags(keyword_text)
                keywords.append(keyword)
            return keywords
        except Exception as e:
            raise e

    def _get_all_data(self):
        """
        Returns all necessary information from the dataset.
        """
        keywords = self._get_keywords()
        print(keywords)

    def scrape(self) -> list:
        """
        Scrapes all necessary information from the dataset.
        """
        self._driver = webdriver.Firefox(
            executable_path=config.SELENIUM_DRIVER_PATH)

        self._driver.get(self.dataset_url)
        time.sleep(self.crawl_delay)
        data = self._get_all_data()

        self._driver.close()
        return data
