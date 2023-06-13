import time
from sentence_transformers import SentenceTransformer
from pymilvus import Collection
import config
from pymilvus import connections

def embed_search(data, transformer):
    embeds = transformer.encode(data) 
    return [x for x in embeds]

def search(query):
    # connect to server
    connections.connect(host=config.MILVUS_HOST, port=config.MILVUS_PORT)

    # load in database
    collection = Collection("movies_db")   
    collection.load()

    # load in transformer
    transformer = SentenceTransformer('all-MiniLM-L6-v2')

    # get embedding
    search_data = embed_search([query], transformer)

    # perform search
    start = time.time()
    res = collection.search(
        data=search_data,  # Embeded search value
        anns_field="embedding",  # Search across embeddings
        param={},
        limit = 3,  # Limit to top_k results per search
        output_fields=['title']  # Include title field in result
    )
    end = time.time()

    # print hits
    for hits_i, hits in enumerate(res):
        print('Title:', query)
        print('Search Time:', end-start)
        print('Results:')
        for hit in hits:
            print( hit.entity.get('title'), '----', hit.distance)
        print()

search("Give me all the datasets that correpond to mental health.")