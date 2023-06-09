from python.scripts.scrape import get_all_dataset_urls, scrape_data


def main():
    #get_all_dataset_urls("resources/urls.txt")
    scrape_data("https://open.canada.ca/data/en/dataset/3ac0d080-6149-499a-8b06-7ce5f00ec56c")


if __name__ == "__main__":
    main()
