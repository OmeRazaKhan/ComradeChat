"""
#TODO Implement _scrape_datasets() and create Dataset class.
"""

import time
import re
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

import python.scrapers.config as config
from python.scrapers.scraper import Scraper
from python.scrapers.dataset_extensions import DatasetExtensions


class DataScraper(Scraper):
    """
    Scrapes all relevant information from a URL containing a dataset.
    """

    def __init__(
        self, dataset_url: str, crawl_delay: float = config.DEFAULT_CRAWL_DELAY
    ):
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
                    (By.XPATH, "/html/body/div/div/main/div[2]/aside/div[2]/ul/li[2]")
                )
            )
            keyword_title_path = keywords_div.find_element(
                by=By.XPATH, value="./strong"
            )
            if not "Keyword" in keyword_title_path.text:
                raise Warning("Did not find keyword section")
            keywords = []
            keywords_ul = keywords_div.find_element(by=By.XPATH, value="./ul")
            WebDriverWait(keywords_ul, 10).until(
                EC.presence_of_element_located((By.XPATH, "./*"))
            )
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
                    (By.XPATH, "/html/body/div/div/main/div[2]/aside/div[2]/ul/li[3]")
                )
            )
            subject_title_path = subjects_div.find_element(
                by=By.XPATH, value="./strong"
            )
            if not "Subject" in subject_title_path.text:
                raise Warning("Did not find subject section")
            subjects = []
            subjects_ul = subjects_div.find_element(by=By.XPATH, value="./ul")
            WebDriverWait(subjects_ul, 10).until(
                EC.presence_of_element_located((By.XPATH, "./*"))
            )
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
                    (By.XPATH, "/html/body/div/div/main/div[2]/aside/div[2]/ul/li[4]")
                )
            )
            audiences_title_path = audiences_div.find_element(
                by=By.XPATH, value="./strong"
            )
            if not "Audience" in audiences_title_path.text:
                raise Warning("Did not find audience section")
            audiences = []
            audiences_ul = audiences_div.find_element(by=By.XPATH, value="./ul")
            WebDriverWait(audiences_ul, 10).until(
                EC.presence_of_element_located((By.XPATH, "./*"))
            )
            audiences_li = audiences_ul.find_elements(by=By.XPATH, value="./*")
            for audience_li in audiences_li:
                audience_text = audience_li.text
                audience = self._strip_html_tags(audience_text)
                audiences.append(audience)
            return audiences
        except Exception as e:
            raise e

    def _scrape_temporal_coverage(self) -> str:
        """
        Scrapes the date of coverage for the news article.

        Raises:
            Warning: If the section could not be identified to have a temporal coverage section.
            Exception: If an element could not be located.

        Returns:
            (str): The temporal period covered by the dataset in the format "yyyy-mm-dd to yyyy-mm-dd".
        """
        try:
            temporal_coverage_div = WebDriverWait(self._driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div/div/main/div[2]/aside/div[2]/ul/li[11]")
                )
            )
            temporal_coverage_title_path = temporal_coverage_div.find_element(
                by=By.XPATH, value="./b"
            )
            if not "Temporal Coverage" in temporal_coverage_title_path.text:
                raise Warning("Did not find temporal coverage section")
            temporal_coverage_field = temporal_coverage_div.find_element(
                by=By.XPATH, value="./small"
            )
            temporal_coverage_text = temporal_coverage_field.text
            temporal_coverage = self._strip_html_tags(temporal_coverage_text)
            return temporal_coverage
        except Exception as e:
            raise e

    def _scrape_dataset_description_texts(self) -> list:
        """
        Scrapes the description given for the dataset.

        Raises:
            Warning: If the section could not be identified to have an audience.
            Exception: If an element could not be located.

        Returns:
            (list): List of all text sections in the dataset description.
        """
        try:
            description_div = WebDriverWait(self._driver, 10).until(
                EC.presence_of_element_located((By.ID, "resource-desc"))
            )
            description_paragraphs = []
            WebDriverWait(description_div, 10).until(
                EC.presence_of_element_located((By.XPATH, "./*"))
            )
            description_children = description_div.find_elements(
                by=By.XPATH, value="./*"
            )
            for child in description_children:
                child_text = child.text
                child = self._strip_html_tags(child_text)
                description_paragraphs.append(child)
            return description_paragraphs
        except Exception as e:
            raise e

    def _parse_resource_information_panel(self, title_panel) -> dict:
        """
        Extracts all relevant information from the title panel in a resource item.
        """
        title_element, information_tag_div = title_panel.find_elements(
            by=By.XPATH, value="./*"
        )
        title = self._strip_html_tags(title_element.text)
        languages = []
        miscellaneous_info = []
        recognized_dataset_extensions = [
            extension.value for extension in DatasetExtensions
        ]
        file_type = None
        for child in information_tag_div.find_elements(by=By.XPATH, value="./*"):
            classes = child.get_attribute("class")
            text = self._strip_html_tags(child.text)
            if "res-tag-lang" in classes:  # See if the tag is a language.
                languages.append(text)
            elif text.lower() in recognized_dataset_extensions:
                if not file_type is None:
                    print(
                        "Warning: Multiple file types detected: {} and {}".format(
                            file_type, text.lower()
                        )
                    )
                file_type = text
            else:
                miscellaneous_info.append(text)

        information_tags = {}
        information_tags["title"] = title
        information_tags["languages"] = languages
        information_tags["file_type"] = file_type
        information_tags["miscellaneous"] = miscellaneous_info
        return information_tags

    def _parse_resource_url(self, download_resource_panel) -> str:
        """
        Returns the URL to download a resource which is relevant to the dataset.
        """
        # print(download_panel.text)
        anchor_tags = download_resource_panel.find_elements(
            by=By.XPATH, value=".//*//a"
        )
        for anchor_tag in anchor_tags:
            text = self._strip_html_tags(anchor_tag.text)
            if text == "Download":
                return anchor_tag.get_attribute("href")

    def _scrape_resources(self) -> list:
        """
        Scrapes all resources relevant to the dataset from the webpage.

        Raises:
            Warning.
            Exception: If an element could not be located.

        Returns:
            (list): A list of all datasets on the webpage.
        """

        try:
            resource_div = WebDriverWait(self._driver, 10).until(
                EC.presence_of_element_located((By.ID, "dataset-resources"))
            )
            resource_ul = resource_div.find_element(by=By.XPATH, value=".//ul")
            all_resources = []
            WebDriverWait(resource_div, 10).until(
                EC.presence_of_element_located((By.XPATH, "./*"))
            )
            resource_items = resource_ul.find_elements(by=By.XPATH, value="./*")
            for resource_item in resource_items:
                resource_dict = dict()
                title_panel, download_panel = resource_item.find_elements(
                    by=By.XPATH, value="./*"
                )
                resource_dict = self._parse_resource_information_panel(title_panel)
                resource_url = self._parse_resource_url(download_panel)
                resource_dict["resource_url"] = resource_url
                all_resources.append(resource_dict)
            return all_resources

        except Exception as e:
            raise e

    def _get_all_data(self) -> dict:
        """
        Returns all necessary information from the dataset.
        """
        dataset = {}
        dataset["dataset_url"] = self._dataset_url

        try:
            dataset["dataset_description"] = self._scrape_dataset_description_texts()
        except Warning as e:
            print(e)
        except Exception as e:
            print("Unable to scrape description.")

        try:
            dataset["keywords"] = self._scrape_keywords()
        except Warning as e:
            print(e)
        except Exception as e:
            print("Unable to scrape keywords.")

        try:
            dataset["subjects"] = self._scrape_subjects()
        except Warning as e:
            print(e)

        try:
            dataset["audience"] = self._scrape_audience()
        except Warning as e:
            print(e)
        except Exception as e:
            print("Unable to scrape audience.")

        try:
            dataset["temporal_coverage"] = self._scrape_temporal_coverage()
        except Warning as e:
            print(e)
        except Exception as e:
            print("Unable to scrape temporal coverage.")

        try:
            dataset["resources"] = self._scrape_resources()
        except Warning as e:
            print(e)
        except Exception as e:
            print("Unable to scrape resource data.")

        return dataset

    def scrape(self) -> dict:
        """
        Scrapes all necessary information from the dataset.
        """
        self._driver = webdriver.Firefox(executable_path=config.SELENIUM_DRIVER_PATH)

        self._driver.get(self.dataset_url)
        time.sleep(self.crawl_delay)
        data = self._get_all_data()

        self._driver.close()
        return data
