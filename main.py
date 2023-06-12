from python.scripts.scrape import get_all_dataset_urls, scrape_data
from python.scripts.parse_metadata import parse_metadata


def main():
    # get_all_dataset_urls("resources/urls.txt")
    # scrape_data(
    #    ["https://open.canada.ca/data/en/dataset/3ac0d080-6149-499a-8b06-7ce5f00ec56c"], "resources/data.json")
    scraped_metadata = parse_metadata("resources/data.json")
    print(scraped_metadata)


if __name__ == "__main__":
    main()
