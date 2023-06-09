from abc import ABC

import python.scrapers.config as config

class Scraper(ABC):
    """
    Performs all scraping operations on the open source data portal.
    """

    def __init__(self, crawl_delay: float):
        """
        Params:
            crawl_delay (float): The delay after loading a new webpage.
        """
        self._crawl_delay = crawl_delay
        self._driver = None

    @property
    def crawl_delay(self) -> float:
        """
        The time delay after loading a new webpage.
        """
        return self._crawl_delay