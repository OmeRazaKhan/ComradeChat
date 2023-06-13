from pymilvus import connections
import config
from pymilvus import utility
from pymilvus import FieldSchema, CollectionSchema, DataType, Collection
from sentence_transformers import SentenceTransformer
import pandas as pd

# connect to server
connections.connect(host=config.MILVUS_HOST, port=config.MILVUS_PORT)

# remove any previous collections with the same name
if utility.has_collection(config.COLLECTION_NAME):
    utility.drop_collection(config.COLLECTION_NAME)

# create collection which includes the id, title, and embedding.
fields = [
    FieldSchema(name='id', dtype=DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema(name='title', dtype=DataType.VARCHAR, max_length=1000),  # VARCHARS need a maximum length, so for this example they are set to 200 characters
    FieldSchema(name='embedding', dtype=DataType.FLOAT_VECTOR, dim=config.DIMENSION)
]

schema = CollectionSchema(fields=fields)
collection = Collection(name=config.COLLECTION_NAME, schema=schema)

# create indices for database
index_params = {
    'metric_type':'L2',
    'index_type':"IVF_FLAT",
    'params':{'nlist': 1536}
}

# create indices for database
collection.create_index(field_name="embedding", index_params=index_params)
collection.load()

# extract embeding from text using OpenAI
def embed_insert(data):
    embeds = transformer.encode(data[1])

    ins = [
            data[0],
            [x for x in embeds]
    ]
    collection.insert(ins)

# load in transformer
transformer = SentenceTransformer('all-MiniLM-L6-v2')

# read in the data
df = pd.read_csv("data.csv")

# insert into database
for index, row in df.iterrows():
    data_batch = [[],[]]

    data_batch[0].append(row["title"])
    data_batch[1].append(row["title"])
    
    embed_insert(data_batch)