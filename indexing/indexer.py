import os
import json
import argparse
import numpy as np
np.float_ = np.float64
from elasticsearch import Elasticsearch, helpers
import time


# **Constants**
# DEST_FILE = "company_data.json"
DATA_FILE = "./posts.json"
ES_INDEX_NAME = "reddit_sports_data"
ES_HOST = "http://localhost:9200"


def load_data(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

# **Step 2: Prepare Data for Elasticsearch**
def prepare_data(data):
    """Extracts text and metadata from JSON data for indexing in Elasticsearch."""
    documents = []

    for obj in data:
        text_data = f"{obj['Subreddit']} {obj['Sports category']} {obj['Title']} {obj['Post Text']}"
        metadata = {
            "subreddit": obj["Subreddit"],
            "subreddit_url": obj["Subreddit URL"],
            "title": obj["Title"],
            "post_text": obj["Post Text"],
            "post_id": obj["ID"],
            "score": obj["Score"],
            "num_comments": obj["Total Comments"],
            "post_url": obj["Post URL"],
            "sport": obj["Sports category"]
        }
        documents.append({"text": text_data, "metadata": metadata})

    return documents


# **Step 3: Create Elasticsearch Index**
def create_es_index(es, index_name):
    """Creates an Elasticsearch index with proper mapping if it does not already exist."""
    mapping = {
        "mappings": {
            "properties": {
                "text": {"type": "text"},
                "metadata": {
                    "properties": {
                        "subreddit": {"type": "text"},
                        "subreddit_url": {"type": "text"},
                        "title": {"type": "text"},
                        "post_text": {"type": "text"},
                        "post_id": {"type": "text"},
                        "score": {"type": "integer"},
                        "num_comments": {"type": "integer"},
                        "post_url": {"type": "text"},
                        "sport": {"type": "text"}
                    }
                },
            }
        }
    }

    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name, body=mapping)
        print(f"✅ Index '{index_name}' created successfully.")
    else:
        print(f"⚠️ Index '{index_name}' already exists.")


# **Step 4: Index Documents in Elasticsearch**
def index_documents_in_es(es, index_name, documents):
    """Indexes a list of documents into Elasticsearch."""
    start_time = time.time()

    actions = [
        {
            "_index": index_name,
            "_id": doc_id,
            "_source": doc,
        }
        for doc_id, doc in enumerate(documents)
    ]

    helpers.bulk(es, actions)
    end_time = time.time()
    print(f"✅ Indexed {len(documents)} documents in Elasticsearch.")
    print(f"Time taken: {(end_time - start_time)/60} minutes")


# **Main Execution**
if __name__ == "__main__":
    os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"  # Prevent duplicate library errors

    print("\n📌 Step 1: Loading JSON data")
    data = load_data(DATA_FILE)

    print("\n📌 Step 2: Preparing data for Elasticsearch")
    documents = prepare_data(data)
    print(f"✅ Prepared {len(documents)} records for indexing.")

    print("\n📌 Step 3: Connecting to Elasticsearch")
    es = Elasticsearch(ES_HOST)


    if es.ping():
        print("✅ Connected to Elasticsearch.")

        print("\n📌 Step 4: Creating Elasticsearch Index")
        create_es_index(es, ES_INDEX_NAME)

        print("\n📌 Step 5: Indexing Data in Elasticsearch")
        index_documents_in_es(es, ES_INDEX_NAME, documents)

    else:
        print("❌ Could not connect to Elasticsearch. Ensure it is running.")
