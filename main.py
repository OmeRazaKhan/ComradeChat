from api.api import API
from python.scripts.scrape import scrape_all_data, scrape_datasets

if __name__ == "__main__":
    #api = API("resources/datasets.json")
    # response = api.generate_response(
    #    "What is the meaning of life?", maximum_num_responses=4)
    # print(response)

    urls = []
    with open("resources/urls.txt", "r") as f:
        for line in f:
            urls.append(line)
    scrape_datasets(urls, "resources/datasets.json", max_num_datasets=2)
