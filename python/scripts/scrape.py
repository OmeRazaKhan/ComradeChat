from python.scrapers.scraper import Scraper


def scrape():
    """
    Scrapes data from the open source portal.
    """
    scraper = Scraper()
    scraper.launch()
    urls = scraper.get_all_dataset_urls()


if __name__ == "__main__":
    scrape()
