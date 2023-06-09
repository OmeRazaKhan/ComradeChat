"""
#TODO
Implement:
        subjects = self._scrape_subjects() #TODO
        audience = self._scrape_audience() #TODO
        date_published = self._scrape_date_published() #TODO
        dataset_description = self._scrape_dataset_description() #TODO
        datasets = self._scrape_datasets() #TODO
"""

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

    def _scrape_keywords(self) -> list:
        """
        Scrapes a list of all keywords about the dataset on a webpage.

        Raises:
            Warning: If the section could not be identified to have keywords.
            Exception: If an element could not be located.

        Returns:
            (list): All keywords found on the dataset's webpage.
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

    def _scrape_subjects(self) -> list:
        """
        Scrapes all relevant subjects listed on the dataset's webpage.

        Raises:
            Warning: If the section could not be identified to have subjects.
            Exception: If an element could not be located.

        Returns:
            (list): A list of all relevant subjects to the dataset.
        """
        try:
            subjects_div = WebDriverWait(self._driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div/div/main/div[2]/aside/div[2]/ul/li[3]"))
            )
            subject_title_path = subjects_div.find_element(
                by=By.XPATH, value="./strong")
            if not "Subject" in subject_title_path.text:
                raise Warning("Did not find subject section")
            subjects = []
            subjects_ul = subjects_div.find_element(by=By.XPATH, value="./ul")
            WebDriverWait(subjects_ul, 10).until(
                EC.presence_of_element_located((By.XPATH, './*')))
            subjects_li = subjects_ul.find_elements(by=By.XPATH, value="./*")
            for subject_li in subjects_li:
                subject_text = subject_li.text
                subject = self._strip_html_tags(subject_text)
                subjects.append(subject)
            return subjects
        except Exception as e:
            raise e

    def _scrape_audience(self) -> list:
        """
        Scrapes all potential audiences listed on the dataset's webpage.

        Raises:
            Warning: If the section could not be identified to have an audience.
            Exception: If an element could not be located.

        Returns:
            (list): A list of all potential audiences for the dataset.
        """
        try:
            audiences_div = WebDriverWait(self._driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div/div/main/div[2]/aside/div[2]/ul/li[4]"))
            )
            audiences_title_path = audiences_div.find_element(
                by=By.XPATH, value="./strong")
            if not "Audience" in audiences_title_path.text:
                raise Warning("Did not find audience section")
            audiences = []
            audiences_ul = audiences_div.find_element(
                by=By.XPATH, value="./ul")
            WebDriverWait(audiences_ul, 10).until(
                EC.presence_of_element_located((By.XPATH, './*')))
            audiences_li = audiences_ul.find_elements(by=By.XPATH, value="./*")
            for audience_li in audiences_li:
                audience_text = audience_li.text
                audience = self._strip_html_tags(audience_text)
                audiences.append(audience)
            return audiences
        except Exception as e:
            raise e

    def _scrape_date_published(self) -> str:
        """
        Scrapes the date that the dataset was published.

        Raises:
            Warning: If the section could not be identified to have an audience.
            Exception: If an element could not be located.

        Returns:
            (str): The dataset's publication date in the format yyyy-mm-dd.
        """

    def _scrape_dataset_description(self) -> str:
        """
        Scrapes the description given for the dataset.

        Raises:
            Warning: If the section could not be identified to have an audience.
            Exception: If an element could not be located.

        Returns:
            (str): The description given for the dataset.
        """

    def _get_all_data(self):
        """
        Returns all necessary information from the dataset.
        """
        keywords = self._scrape_keywords()  # Complete
        subjects = self._scrape_subjects()  # Complete
        audience = self._scrape_audience()  # TODO
        date_published = self._scrape_date_published()  # TODO
        dataset_description = self._scrape_dataset_description()  # In progress
        # datasets = self._scrape_datasets() #In progress

        print(audience)

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
