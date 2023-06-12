from python.scripts.scrape import get_all_dataset_urls, scrape_data
from python.scripts.parse_metadata import parse_metadata
from python.database.parser import Parser
from python.database.database import Database


def main():
    # get_all_dataset_urls("resources/urls.txt")
    # scrape_data(
    #    ["https://open.canada.ca/data/en/dataset/3ac0d080-6149-499a-8b06-7ce5f00ec56c"], "resources/data.json")
    parser = Parser()
    all_metadata = parser.parse("resources/data.json")
    #scraped_metadata = parse_metadata("resources/data.json")
    db = Database(all_metadata)
    print(db.get_all_descriptions())


if __name__ == "__main__":
    main()
