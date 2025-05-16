import numpy as np
np.float_ = np.float64
from elasticsearch import Elasticsearch

# Connect to Elasticsearch
es = Elasticsearch("http://localhost:9200")

# Function to search documents
def search_documents(index_name, query, count=10):
    search_query = {
        "query": {
            "query_string": {
                "query": query  # General query for full-text search across all fields
            }
        }
    }

    response = es.search(index=index_name, body=search_query, size=count)
    
    data = []
    # Print search results
    if response['hits']['hits']:
        print(f"\nFound {len(response['hits']['hits'])} results for '{query}':\n")
        for hit in response['hits']['hits']:
            print(f"ID: {hit['_id']} | Matching Score: {hit['_score']}")
            val = hit['_source']
            print(f"Source: {val}\n")
            data.append(val)
    else:
        print(f"No results found for '{query}'.")

# Run the search
if __name__ == "__main__":
    index_name = 'reddit_sports_data'
    while True:
        print("Type exit to quit")
        count = int(input("Enter number of results to return: "))
        query = input("Enter query to search DB: ")
        if query =="exit":
            break
        else:
            search_documents(index_name, query, count)
