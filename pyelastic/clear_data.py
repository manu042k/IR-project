import numpy as np
np.float_ = np.float64
from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")
index_name = "reddit_sports_data"

if es.ping():
    es.indices.delete(index=index_name, ignore=[400, 404])
    print(f"✅ Index '{index_name}' and all its data have been deleted.")
else:
    print("❌ Could not connect to Elasticsearch. Ensure it is running.")
