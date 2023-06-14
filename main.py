from python.scripts.scrape import get_all_dataset_urls, scrape_data
from python.scripts.parse_metadata import parse_metadata
from python.database.parser import Parser
from python.database.database import Database
from milvus_db.setup_database import setup_db
from milvus_db.predict import search

def main():
    # get_all_dataset_urls("resources/urls.txt")
    # scrape_data(
    #    ["https://open.canada.ca/data/en/dataset/3ac0d080-6149-499a-8b06-7ce5f00ec56c"], "resources/data.json")
    parser = Parser()
    all_metadata = parser.parse("resources/data.json")
    # #scraped_metadata = parse_metadata("resources/data.json")
    db = Database(all_metadata)
    print(db.get_all_descriptions())
    


    # data = {
    #     "1": "Binder used by the Chief of the Defence Staff to support his appearance on Arctic Security in front of the House Standing Committee on National Defence.",
    #     "2": "The dataset contains the list of sites across Canada where unexploded explosive ordnance have been located or may be present and are being assessed.",
    #     "3": "Suicide is a tragedy and an important public health concern. Suicide prevention is a top priority for the Canadian Armed Forces (CAF). Monitoring and analyzing suicide events of CAF members provides valuable information to guide and refine ongoing suicide prevention efforts. The dataset shows the comparison of CAF regular force male members suicide rates by deployment history to Canadian rates using standardized mortality ratios from 1995 to 2019.",
    #     "4": "This dataset shows the Canadian Armed Forces (CAF) rate for suicide per 100,000 for Regular Force males. As the number of events was less than 20 in most years, rates were not calculated annually as these would not have been statistically reliable. Regular Force female rates were not calculated because female suicides were uncommon. This dataset is taken from the yearly Report on Suicide Mortality in the Canadian Armed Forces released on the Canada.ca platform at the homepage link provided down below.",
    #     "5": "List of internal Department of National Defence and Canadian Armed Forces forms. This dataset does not provide public access to the forms because they are for internal use only. The forms are ONLY available and accessible through the Department of National Defence and the Canadian Armed Forces intranet (DWAN) at the homepage link provided below on this page.",
    #     "6": "Canadian Armed Forces operate various modern military vehicles, including the latest in armoured, recovery, engineering and reconnaissance vehicles. This dataset contains a listing of all Canadian Armed Forces vehicle equipment.",
    #     "7": "In accordance with the Treasury Board Directive on Internal Audit, the Department of National Defence and the Canadian Armed Forces publishes key performance results for its internal audit function. These results, or key compliance attributes, demonstrate that the fundamental elements necessary for oversight are in place in the organization, are performing and are achieving results.",
    #     "8": "This dataset list the total number of military and civilian personnel from 2001-2022. The dataset is separated in the following categories: gender, regular forces, reserve forces, officer and non-commissioned member (NCM).",
    #     "9": "This dataset represents the number of promotions for Non-Commissioned Members (NCMs) in the Canadian Armed Forces (CAF) Regular Force by Gender from 1998 to 2022. Military Personnel Command (MPC) supports the requirement to release accurate and timely information to Canadians, in line with the principles of Open Government. MPC has made every attempt to ensure the accuracy and reliability of the information provided. However, data contained within this report may also appear in historic, current and future reports of a similar nature where it may be represented differently, and in some cases appear to be in conflict with the current",
    #     "10": "This dataset represents the number of promotions for Officers in the Canadian Armed Forces (CAF) Regular Force by Gender from 1998 to 2022. Military Personnel Command (MPC) supports the requirement to release accurate and timely information to Canadians, in line with the principles of Open Government. MPC has made every attempt to ensure the accuracy and reliability of the information provided. However, data contained within this report may also appear in historic, current and future reports of a similar nature where it may be represented differently, and in some cases appear to be in conflict with the current report."
    # }
    
    # setup_db(data) # the data argument is the dictionary of the 150 entries of id: description. This sets up the database by embedding all the vectors. This will be called once at the start.
    
    # search("Suicide is a tragedy and an important public health concern. Suicide prevention i") # this is the user's query. it will return an array of ids. This will be called everytime the user types something in.

if __name__ == "__main__":
    api = API("resources/datasets.json")
    response = api.generate_response(
        "What is the meaning of life?", maximum_num_responses=4)
    print(response)

    #urls = []
    # with open("resources/urls.txt", "r") as f:
    #    for line in f:
    #
    #        #Chop newline character if needed
    #        if line[len(line) - 1] == "\n":
    #            urls.append(line[:len(line) - 1])
    #        else:
    #            urls.append(line)
    #scrape_datasets(urls, "resources/datasets.json", max_num_datasets=2)
