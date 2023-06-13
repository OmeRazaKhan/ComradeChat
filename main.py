from api.api import API
from python.scripts.scrape import get_all_dataset_urls, scrape_data


def scrape():
    """
    Scrapes all website data.
    """
    get_all_dataset_urls("resources/urls.txt")
    scrape_data(
        ["https://open.canada.ca/data/en/dataset/3ac0d080-6149-499a-8b06-7ce5f00ec56c"], "resources/data.json")


if __name__ == "__main__":
    api = API("resources/data.json")
    response = api.generate_response(
        "What is the meaning of life?", maximum_num_responses=4)
    print(response)
