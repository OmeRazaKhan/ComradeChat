from api.api import API
from python.scripts.scrape import scrape_all_data

if __name__ == "__main__":
    api = API("resources/datasets.json")
    response = api.generate_response(
        "What is the meaning of life?", maximum_num_responses=4)
    print(response)

    #scrape_all_data("urls.txt", "resources/datasets.json")
