#!/usr/bin/env python3
"""
Reddit Sports Data Indexer

This module indexes Reddit sports data from a JSON file into Elasticsearch.
It creates an index with appropriate mappings and bulk indexes the documents.
"""

import os
import json
import time
from elasticsearch import Elasticsearch, helpers
import numpy as np

# Fix for numpy float type compatibility
np.float_ = np.float64

# Configuration variables (from environment or defaults)
DATA_FILE = os.getenv("DATA_FILE", "./posts.json")
ES_INDEX_NAME = os.getenv("ES_INDEX_NAME", "reddit_sports_data")
ES_HOST = os.getenv("ES_HOST", "http://localhost:9200")


def load_data(file_path):
    """
    Load JSON data from the specified file.
    
    Args:
        file_path (str): Path to the JSON data file
        
    Returns:
        list: Loaded JSON data
    """
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data
def prepare_data(data):
    """
    Extracts text and metadata from JSON data for indexing in Elasticsearch.
    
    Args:
        data (list): List of Reddit post objects
        
    Returns:
        list: Documents prepared for Elasticsearch indexing
    """
    documents = []

    for obj in data:
        # Combine important fields for text search
        text_data = f"{obj['Subreddit']} {obj['Sports category']} {obj['Title']} {obj['Post Text']}"
        
        # Extract and organize metadata
        metadata = {
            "subreddit": obj["Subreddit"],
            "subreddit_url": obj["Subreddit URL"],
            "title": obj["Title"],
            "post_text": obj["Post Text"],
            "post_id": obj["ID"],
            "score": obj["Score"],
            "num_comments": obj["Total Comments"],
            "post_url": obj["Post URL"],
            "sport": obj["Sports category"],
            "upvote_ratio": obj.get("Upvote Ratio", 0),
            "awards": obj.get("Awards", 0),
            "time": obj.get("Time", "")
        }
        documents.append({"text": text_data, "metadata": metadata})

    return documents


def create_es_index(es, index_name):
    """
    Creates an Elasticsearch index with proper mapping if it does not already exist.
    
    Args:
        es (Elasticsearch): Elasticsearch client instance
        index_name (str): Name of the index to create
    """
    # Define index mapping with appropriate field types
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
                        "sport": {"type": "text"},
                        "upvote_ratio": {"type": "float"},
                        "awards": {"type": "integer"},
                        "time": {"type": "date", "format": "yyyy-MM-dd HH:mm:ss||strict_date_optional_time"}
                    }
                },
            }
        }
    }

    # Create index if it doesn't exist
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name, body=mapping)
        print(f"✅ Index '{index_name}' created successfully.")
    else:
        print(f"⚠️ Index '{index_name}' already exists.")


def index_documents_in_es(es, index_name, documents):
    """
    Indexes a list of documents into Elasticsearch using bulk indexing.
    
    Args:
        es (Elasticsearch): Elasticsearch client instance
        index_name (str): Name of the index to use
        documents (list): List of documents to index
    """
    start_time = time.time()
    
    # Prepare bulk indexing actions
    actions = [
        {
            "_index": index_name,
            "_id": doc_id,
            "_source": doc,
        }
        for doc_id, doc in enumerate(documents)
    ]

    # Execute bulk indexing
    helpers.bulk(es, actions)
    
    # Report completion stats
    end_time = time.time()
    elapsed_minutes = (end_time - start_time) / 60
    print(f"✅ Indexed {len(documents)} documents in Elasticsearch.")
    print(f"Time taken: {elapsed_minutes:.2f} minutes")

def execute_indexing():
    """
    Main function to execute the indexing process.
    
    Returns:
        str: Message indicating success or failure
    """
    start_time_total = time.time()
    try:
        # Step 1: Load data from JSON file
        print("\n📌 Step 1: Loading JSON data")
        data = load_data(DATA_FILE)

        # Step 2: Process data for indexing
        print("\n📌 Step 2: Preparing data for Elasticsearch")
        documents = prepare_data(data)
        print(f"✅ Prepared {len(documents)} records for indexing.")

        # Step 3: Connect to Elasticsearch
        print("\n📌 Step 3: Connecting to Elasticsearch")
        es = Elasticsearch(ES_HOST)

        if es.ping():
            print("✅ Connected to Elasticsearch.")

            # Step 4: Create or verify index exists
            print("\n📌 Step 4: Creating Elasticsearch Index")
            create_es_index(es, ES_INDEX_NAME)

            # Step 5: Index documents
            print("\n📌 Step 5: Indexing Data in Elasticsearch")
            index_documents_in_es(es, ES_INDEX_NAME, documents)
            
            # Calculate total execution time
            end_time_total = time.time()
            time_taken_seconds = end_time_total - start_time_total
            return f"✅ Indexing completed successfully. Total time taken: {time_taken_seconds:.2f} seconds"

        else:
            print("❌ Could not connect to Elasticsearch. Ensure it is running.")
            raise Exception("❌ Could not connect to Elasticsearch.")
    except Exception as e:
        print(f"❌ An error occurred: {e}")
        raise

def main():
    """Entry point for script execution"""
    # Prevent duplicate library errors (common with numpy on some systems)
    os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
    
    # Execute the indexing process and print result
    result = execute_indexing()
    print(result)


if __name__ == "__main__":
    main()