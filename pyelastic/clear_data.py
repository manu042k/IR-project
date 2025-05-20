import os
import numpy as np
np.float_ = np.float64
from elasticsearch import Elasticsearch

def clear_elasticsearch_index(index_to_delete="reddit_sports_data"):
    """
    Deletes the specified Elasticsearch index if the client can connect.

    Args:
        es_client: An instance of the Elasticsearch client.
        index_to_delete: The name of the index to delete.
    """
    es_client = Elasticsearch(os.getenv("ES_HOST", "http://localhost:9200"))
    if es_client.ping():
        es_client.indices.delete(index=index_to_delete, ignore=[400, 404])
        print(f"✅ Index '{index_to_delete}' and all its data have been deleted.")
    else:
        print("❌ Could not connect to Elasticsearch. Ensure it is running.")

if __name__ == "__main__":
    
    index_name = "reddit_sports_data"
    clear_elasticsearch_index(es, index_name)
