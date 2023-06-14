from pymilvus import connections
from pymilvus import utility
from pymilvus import FieldSchema, CollectionSchema, DataType, Collection
from sentence_transformers import SentenceTransformer
import milvus_db.config as config
import pandas as pd


# extract embeding from text using huggingface
def embed_insert(data, collection) -> None:
    # load in transformer
    transformer = SentenceTransformer("all-MiniLM-L6-v2")

    # There has to be multiple descriptions in array
    embeds = transformer.encode(data[1])

    ins = [data[0], [x for x in embeds]]
    collection.insert(ins)


def setup_db(data) -> None:
    # connect to server
    connections.connect(host=config.MILVUS_HOST, port=config.MILVUS_PORT)

    # remove any previous collections with the same name
    if utility.has_collection(config.COLLECTION_NAME):
        utility.drop_collection(config.COLLECTION_NAME)

    # create collection which includes the id, title, and embedding.
    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
        FieldSchema(name="dict_id", dtype=DataType.INT64),  # id from dictionary
        # FieldSchema(name='title', dtype=DataType.VARCHAR, max_length=1000),  # VARCHARS need a maximum length, so for this example they are set to 200 characters
        FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=384),
    ]

    schema = CollectionSchema(fields=fields)
    collection = Collection(name=config.COLLECTION_NAME, schema=schema)

    # create indices for database
    index_params = {
        "metric_type": "L2",
        "index_type": "IVF_FLAT",
        "params": {"nlist": 1536},
    }

    # create indices for database
    collection.create_index(field_name="embedding", index_params=index_params)
    collection.load()

    # insert into database
    for index, data in data.items():
        data_batch = [[], []]

        data_batch[0].append(int(index))
        data_batch[1].append(data)

        embed_insert(data_batch, collection)


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
