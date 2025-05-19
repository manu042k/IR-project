# filepath: /Users/manu042k/Documents/Assignment/Info Retrival/IR-project/pyelastic/search_index.py
import numpy as np
import datetime
import json
from urllib.parse import quote_plus
np.float_ = np.float64
from elasticsearch import Elasticsearch
import os

# Connect to Elasticsearch

# Get Elasticsearch URL from environment variable
ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")

es = Elasticsearch(ELASTICSEARCH_URL)

# Function to calculate a PageRank-inspired score
def calculate_pagerank_score(posts, damping_factor=0.85):
    """
    Calculate a simplified PageRank-inspired score for Reddit posts.
    
    In this simplified model:
    - Posts with more comments are considered more "linked to"
    - Posts with higher scores (votes) are considered more authoritative
    - The damping factor works similarly to traditional PageRank
    
    Parameters:
    - posts: List of post data from Elasticsearch
    - damping_factor: Damping factor (default 0.85)
    
    Returns:
    - Dictionary mapping post IDs to their PageRank scores
    """
    # Initialize scores
    scores = {}
    post_ids = []
    
    # Extract necessary data and assign initial scores
    for post in posts:
        post_id = post.get('_id', '')
        metadata = post.get('_source', {}).get('metadata', {})
        post_ids.append(post_id)
        
        # Initial score based on number of comments (links) and votes
        comment_factor = np.log1p(metadata.get('num_comments', 0))
        vote_factor = np.log1p(metadata.get('score', 0))
        
        # Initial score is weighted combination of comments and votes
        scores[post_id] = 0.5 * comment_factor + 0.5 * vote_factor
    
    # Normalize initial scores
    total_score = sum(scores.values()) or 1  # Avoid division by zero
    for post_id in scores:
        scores[post_id] /= total_score
    
    # Run simplified PageRank iterations
    iterations = 10  # Usually 10-20 iterations is enough for convergence
    for _ in range(iterations):
        new_scores = {post_id: (1 - damping_factor) / len(posts) for post_id in post_ids}
        
        # Each post distributes its score to others based on comment count similarity
        for i, post1 in enumerate(posts):
            post1_id = post1.get('_id', '')
            post1_metadata = post1.get('_source', {}).get('metadata', {})
            post1_comments = post1_metadata.get('num_comments', 0)
            
            outgoing_score = 0
            for j, post2 in enumerate(posts):
                if i == j:
                    continue
                    
                post2_id = post2.get('_id', '')
                post2_metadata = post2.get('_source', {}).get('metadata', {})
                post2_comments = post2_metadata.get('num_comments', 0)
                
                # Similarity based on comments (link strength)
                # We use a simple heuristic: normalize by the maximum comments
                similarity = min(post1_comments, post2_comments) / max(max(post1_comments, post2_comments), 1)
                
                new_scores[post2_id] += damping_factor * scores[post1_id] * similarity
                outgoing_score += similarity
            
            # If no outgoing links, distribute evenly
            if outgoing_score < 0.001:
                for post2_id in post_ids:
                    if post1_id != post2_id:
                        new_scores[post2_id] += damping_factor * scores[post1_id] / (len(posts) - 1)
        
        # Update scores
        scores = new_scores
    
    return scores

# Function to search documents
def search_documents(query, index_name = os.getenv("ES_INDEX_NAME", "reddit_sports_data"), count=10, sort_method="relevance", weight_relevance=1.0, weight_score=1.0, weight_time=1.0, use_pagerank=False):
    """
    Search documents with flexible ranking options.
    
    Parameters:
    - query: Search query string
    - index_name: The Elasticsearch index name
    - count: Number of results to return
    - sort_method: Ranking method ('relevance', 'score', 'time', 'combined')
    - weight_relevance: Weight for relevance score when using 'combined' method
    - weight_score: Weight for vote score when using 'combined' method
    - weight_time: Weight for recency when using 'combined' method
    - use_pagerank: Whether to apply PageRank-inspired ranking to results
    """
    # Base query
    search_query = {
        "query": {
            "query_string": {
                "query": query  # General query for full-text search across all fields
            }
        },
        "size": count
    }
    
    # Apply sorting based on method
    if sort_method == "score":
        # Sort by Reddit score (votes)
        search_query["sort"] = [{"metadata.score": {"order": "desc"}}]
        
    elif sort_method == "time":
        # Sort by post time (most recent first)
        search_query["sort"] = [{"metadata.time": {"order": "asc"}}]
        
    elif sort_method == "combined":
        # Use function_score to create a custom ranking
        search_query = {
            "query": {
                "function_score": {
                    "query": {"query_string": {"query": query}},
                    "functions": [
                        # Relevance is already factored in by the base score
                        # Score (upvotes) factor
                        {
                            "field_value_factor": {
                                "field": "metadata.score",
                                "factor": weight_score,
                                "modifier": "log1p",  # log(1 + score) to reduce impact of extremely high scores
                                "missing": 1
                            }
                        },
                        # Time factor - boost recent posts
                        {
                            "gauss": {
                                "metadata.time": {
                                    "scale": "30d",  # Posts within 30 days get higher boost
                                    "decay": 0.5,
                                    "offset": "7d"
                                }
                            },
                            "weight": weight_time
                        }
                    ],
                    "boost_mode": "multiply",  # Multiply the relevance score by our custom factors
                    "score_mode": "sum"  # Sum up the function scores
                }
            },
            "size": count
        }
    
    # Execute search
    response = es.search(index=index_name, body=search_query)
    
    data = []
    # Process search results
    if response['hits']['hits']:
        results = response['hits']['hits']
        
        # Apply PageRank-inspired ranking if requested
        if use_pagerank:
            # Calculate pagerank scores
            pagerank_scores = calculate_pagerank_score(results)
            
            # Re-sort results based on PageRank scores
            results.sort(key=lambda hit: pagerank_scores.get(hit.get('_id', ''), 0), reverse=True)
            
            ranking_method = f"{sort_method} with PageRank re-ranking"
        else:
            ranking_method = sort_method
        
        print(f"\nFound {len(results)} results for '{query}':\n")
        print(f"Ranking method: {ranking_method}\n")
        
        # Display results
        for hit in results:
            val = hit['_source']
            metadata = val.get('metadata', {})
            # Extract metadata fields
            hit_details = {
                'id': hit['_id'],
                'elasticsearch_score': hit['_score'],
                # Add all metadata fields (title, subreddit, score, comments, time, etc.)
                **metadata
            }

            # Add PageRank score if applicable
            if use_pagerank:
                # pagerank_scores dictionary is computed if use_pagerank is True
                hit_details['pagerank_score'] = pagerank_scores.get(hit.get('_id', ''), 0.0)
            else:
                hit_details['pagerank_score'] = None  # Set to None if PageRank was not used
            
            data.append(hit_details)
    else:
        print(f"No results found for '{query}'.")
        
    return data

# Helper function to explain ranking methods
def explain_ranking_methods():
    print("\n=== Available Ranking Methods ===")
    print("1. relevance: Elasticsearch's default text relevance algorithm")
    print("2. score: Sort by Reddit post score/votes (descending)")
    print("3. time: Sort by post time (most recent first)")
    print("4. combined: Custom ranking combining relevance, score, and time")
    print("   (You'll be able to set weights for each factor)")
    print("\nPageRank Option:")
    print("- You can apply PageRank-inspired ranking to any of the above methods")
    print("- This ranking considers both the number of comments and vote scores")
    print("- Posts that are more 'linked to' (more comments) and with higher scores")
    print("  will receive higher PageRank scores\n")

# Run the search
if __name__ == "__main__":
    index_name = 'reddit_sports_data'
    
    print("\n=== Reddit Sports Data Search Engine ===")
    explain_ranking_methods()
    
    while True:
        print("\n===================================")
        print("Type 'exit' to quit, 'help' for ranking explanations")
        query = input("Enter query to search DB: ")
        
        if query.lower() == "exit":
            break
        elif query.lower() == "help":
            explain_ranking_methods()
            continue
            
        # Get search parameters
        try:
            count = int(input("Enter number of results to return: "))
            
            print("\nSelect ranking method:")
            print("1. relevance  2. score  3. time  4. combined")
            sort_choice = input("Enter choice (1-4) [default: 1]: ").strip()
            
            # Map choices to sort methods
            sort_method_map = {
                "1": "relevance", 
                "2": "score", 
                "3": "time", 
                "4": "combined"
            }
            
            # Default to relevance if empty input
            sort_method = sort_method_map.get(sort_choice, "relevance")
            
            # Get weights if combined method selected
            weight_relevance = 1.0
            weight_score = 1.0
            weight_time = 1.0
            
            if sort_method == "combined":
                print("\nEnter weights for combined ranking (0.1-10.0):")
                weight_relevance = float(input("Relevance weight [default: 1.0]: ") or 1.0)
                weight_score = float(input("Score/votes weight [default: 1.0]: ") or 1.0)
                weight_time = float(input("Recency weight [default: 1.0]: ") or 1.0)
                
                # Validate weights
                for w in [weight_relevance, weight_score, weight_time]:
                    if not (0.1 <= w <= 10.0):
                        print("Weight must be between 0.1 and 10.0. Using default weights.")
                        weight_relevance = weight_score = weight_time = 1.0
                        break
            
            # Ask if user wants to use PageRank
            use_pagerank = input("\nApply PageRank-inspired ranking? (y/n) [default: n]: ").lower().strip() == "y"
            
            if use_pagerank:
                print("PageRank-inspired ranking will be applied to the search results.")
            
            # Execute search with selected parameters
            data = search_documents(
                query,
                index_name, 
                count, 
                sort_method, 
                weight_relevance, 
                weight_score, 
                weight_time,
                use_pagerank
            ) 
            print(f"\n{len(data)} documents returned.")
            print("Data:", json.dumps(data, indent=2))
                
        except ValueError:
            print("Please enter valid numeric values.")
        except Exception as e:
            print(f"Error: {e}")
            print("Please try again.")
