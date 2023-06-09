from python.scrapers.url_scraper import UrlScraper
from python.scrapers.dataset_scraper import DataScraper
from python.scrapers.config import FIRST_PAGE_OPEN_DATA_PORTAL_URL


def get_all_dataset_urls(output_file_path: str, max_num_urls: int = None):
    """
    Retrieves all datasets from the Open Search Portal.

    Params:
        output_file_path (str): The path to the file where the URLs should be outputted.
        num_urls (int, default=None): The maximum number of URLs to obtain.
    """
    scraper = UrlScraper()
    urls = scraper.get_all_dataset_urls(
        FIRST_PAGE_OPEN_DATA_PORTAL_URL, max_num_urls)
    with open(output_file_path, "w", encoding="utf-8") as f:
        for url in urls:
            f.write(url + "\n")


def scrape_data(url: str):
    scraper = DataScraper(url)
    scraper.scrape()
