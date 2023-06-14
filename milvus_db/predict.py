import time
from sentence_transformers import SentenceTransformer
from pymilvus import Collection
from pymilvus import connections
import milvus_db.config as config


def embed_search(data, transformer):
    embeds = transformer.encode(data)
    return [x for x in embeds]


def search(query) -> list[int]:
    # connect to server
    connections.connect(host=config.MILVUS_HOST, port=config.MILVUS_PORT)

    # load in database
    collection = Collection(config.COLLECTION_NAME)
    collection.load()

    # load in transformer
    transformer = SentenceTransformer("all-MiniLM-L6-v2")

    # get embedding
    search_data = embed_search([query], transformer)

    # perform search
    res = collection.search(
        data=search_data,  # Embeded search value
        anns_field="embedding",  # Search across embeddings
        param={},
        limit=3,  # Limit to top_k results per search
        output_fields=["dict_id"],  # Include title field in result
    )

    output = []

    # print hits
    for hits in res:
        # print('Title:', query)
        # print('Search Time:', end-start)
        # print('Results:')
        for hit in hits:
            output.append(hit.entity.get("dict_id"))
            # print( hit.entity.get('dict_id'), '----', hit.distance)

    return output


# print(search("Canadian Armed Forces operate various modern military vehicles, including the latest in armoured, recovery, engineering ."))
