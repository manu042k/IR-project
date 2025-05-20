import os
from fastapi import FastAPI, Query
import uvicorn
from elasticsearch import Elasticsearch
import numpy as np
np.float_ = np.float64
from typing import Optional
from clear_data import clear_elasticsearch_index
from indexer import execute_indexing
from search_index import search_documents
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
# CORS (Cross-Origin Resource Sharing) middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

@app.get("/trigger_indexer")
async def trigger_indexer():
    """
    API endpoint to trigger the indexing process.
    
    Returns:
        A JSON response with the indexing result or error details.
    """
    try:
        result = execute_indexing()
        return {"status": "success", "message": result}
    except Exception as e:
        # Log the error (you might want to add proper logging here)
        error_message = str(e)
        print(f"Error during indexing: {error_message}")
        return {"status": "error", "message": f"Indexing failed: {error_message}"}

@app.delete("/clear-index")
async def clear_index():
    """
    API endpoint to clear the specified Elasticsearch index.
    
    Args:
        index_name: The name of the index to delete. Default is "reddit_sports_data".
        
    Returns:
        A JSON response indicating success or failure.
    """
    try:
        clear_elasticsearch_index()
        return {"status": "success", "message": f"Indexes have been cleared"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.get("/search")
async def search(
    query: str = Query(..., description="Search query string"),
    count: int = Query(10, description="Number of results to return"),
    sort_method: str = Query("relevance", description="Ranking method: 'relevance', 'score', 'time', or 'combined'"),
    weight_relevance: float = Query(1.0, description="Weight for relevance score when using 'combined' method"),
    weight_score: float = Query(1.0, description="Weight for vote score when using 'combined' method"),
    weight_time: float = Query(1.0, description="Weight for recency when using 'combined' method"),
    use_pagerank: bool = Query(False, description="Whether to apply PageRank-inspired ranking to results"),
):
    """
    Search documents in Elasticsearch with flexible ranking options.
    
    Args:
        query: Search query string
        count: Number of results to return
        sort_method: Ranking method ('relevance', 'score', 'time', 'combined')
        weight_relevance: Weight for relevance score when using 'combined' method
        weight_score: Weight for vote score when using 'combined' method
        weight_time: Weight for recency when using 'combined' method
        use_pagerank: Whether to apply PageRank-inspired ranking to results
        index_name: The name of the Elasticsearch index to search
        
    Returns:
        A JSON response with the search results or error details.
    """
    try:
        # Validate inputs
        if sort_method not in ["relevance", "score", "time", "combined"]:
            return {"status": "error", "message": "Invalid sort_method. Must be one of: relevance, score, time, combined"}
        
        if count < 1:
            return {"status": "error", "message": "Count must be greater than 0"}
            
        # Validate weights are within reasonable range
        for weight, name in [(weight_relevance, "weight_relevance"), 
                            (weight_score, "weight_score"), 
                            (weight_time, "weight_time")]:
            if not (0.1 <= weight <= 10.0):
                return {"status": "error", "message": f"{name} must be between 0.1 and 10.0"}
        
        # Call the search_documents function
        index_name = os.getenv("ES_INDEX_NAME", "reddit_sports_data")
        results = search_documents(
            index_name=index_name,
            query=query,
            count=count,
            sort_method=sort_method,
            weight_relevance=weight_relevance,
            weight_score=weight_score,
            weight_time=weight_time,
            use_pagerank=use_pagerank
        )
        
        return {
            "status": "success", 
            "message": f"Found {len(results)} results", 
            "count": len(results),
            "query": query,
            "sort_method": sort_method,
            "use_pagerank": use_pagerank,
            "data": results
        }
        
    except Exception as e:
        error_message = str(e)
        print(f"Error during search: {error_message}")
        return {"status": "error", "message": f"Search failed: {error_message}"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)