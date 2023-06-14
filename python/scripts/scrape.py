import json

from python.scrapers.url_scraper import UrlScraper
from python.scrapers.dataset_scraper import DataScraper
from python.scrapers.config import FIRST_PAGE_OPEN_DATA_PORTAL_URL


def scrape_all_data(
    url_output_file_path: str,
    dataset_output_file_path: str,
    max_num_datasets: int = None,
):
    """
    Scrapes all website data.

    Params:
        url_output_file_path (str): The file path to the txt file where the list of all dataset urls should be written.
        dataset_output_file_path (str): The file path to the JSON file where all dataset information should be written.
        max_num_datasets (int, default=None): The maximum number of datasets to be scraped.
            If None, all datasets will be scraped.
    """
    urls = scrape_urls(url_output_file_path, max_num_urls=max_num_datasets)
    datasets = scrape_datasets(urls, dataset_output_file_path)


def scrape_urls(url_output_file_path: str, max_num_urls: int = None) -> list:
    """
    Retrieves all dataset URLs from the Open Search Portal and writes them to a txt file.

    Params:
        url_output_file_path (str): The path to the txt file where all scraped URLs should be written.
        num_urls (int, default=None): The maximum number of URLs to obtain.

    Returns:
        (list): A list of all URLs leading to datasets in the open search portal.
    """
    scraper = UrlScraper()
    urls = scraper.get_all_dataset_urls(FIRST_PAGE_OPEN_DATA_PORTAL_URL, max_num_urls)
    with open(url_output_file_path, "w", encoding="utf-8") as f:
        for url in urls:
            f.write(url + "\n")
    return urls


def scrape_datasets(
    urls: list, dataset_output_file_path: str, max_num_datasets: int = None
) -> dict:
    """
    Scrapes all datasets from the given urls and stores it in a JSON file.

    Params:
        urls (list): A list of URLs to datasets from which data should be scraped.
        dataset_output_file_path (str): The path to the JSON file where all scraped dataset information should be written.
        max_num_datasets (int, default=None): The maximum number of datasets to obtain.

    Returns:
        (dict): All scraped web data.
    """
    all_data = {}
    print("Scraping Datasets")
    num_datasets = len(urls)
    if not max_num_datasets is None and max_num_datasets < num_datasets:
        num_datasets = max_num_datasets

    for i in range(len(urls)):
        url = urls[i]
        print("Progress: Row {} of {} - Scraping {}".format(i + 1, num_datasets, url))
        scraper = DataScraper(url)
        data = scraper.scrape()
        all_data[i + 1] = data
        if i + 1 >= num_datasets:
            break
    with open(dataset_output_file_path, "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=4)
    return all_data
