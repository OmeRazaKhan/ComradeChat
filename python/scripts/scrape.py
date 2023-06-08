from python.scrapers.scraper import Scraper


def scrape():
    """
    Scrapes data from the open source portal.
    """
    scraper = Scraper()
    scraper.launch()


if __name__ == "__main__":
    scrape()
