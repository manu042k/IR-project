# Reddit Sports Data Search Engine

This project implements a search engine for Reddit sports data, leveraging Elasticsearch for efficient indexing and retrieval. It offers various ranking methods, including traditional relevance, sorting by popularity (score) or recency (time), and a customizable combined ranking approach. Additionally, a PageRank-inspired algorithm can be applied to re-rank results, prioritizing posts with more engagement (comments and votes).

This directory contains scripts and configuration files for indexing, searching, and managing Reddit post data using Elasticsearch. Below is a detailed description of each file:

---

- **README.md**  
  This documentation file. It provides an overview of the contents and purpose of the `pyelastic` directory.

- **main.py**  
  The main entry point for running Elasticsearch-related operations. It typically orchestrates the indexing and searching processes, calling functions from other scripts as needed.

- **indexer.py**  
  Contains functions and logic to index Reddit post data (such as from `posts.json`) into an Elasticsearch index. Handles data transformation and communication with the Elasticsearch server.

- **search_index.py**  
  Provides search functionality over the Elasticsearch index. Contains functions to query the index for relevant Reddit posts based on user queries or search parameters.

- **clear_data.py**  
  Utility script to delete or clear data from the Elasticsearch index. Useful for resetting the index or removing outdated data.

- **posts.json**  
  A sample or working dataset of Reddit posts to be indexed and searched. This file is used as input for the indexing process.

- **docker-compose.yaml**  
  Configuration file for Docker Compose. Defines services (such as Elasticsearch and Kibana) required for running the search infrastructure locally in containers. Simplifies setup and management of the Elasticsearch environment.

---

This structure enables efficient indexing, searching, and management of Reddit post data using Elasticsearch, with scripts for each major operation and a Docker Compose file for easy environment setup.

## search_index.py: Search and Ranking Algorithm Details

The `search_index.py` script implements advanced search and ranking algorithms for retrieving Reddit posts from an Elasticsearch index. Below is a detailed explanation of the algorithms and ranking logic used:

### 1. Flexible Ranking Methods

The script supports multiple ranking strategies for search results:

- **Relevance**: Uses Elasticsearch's default full-text relevance scoring (BM25).
- **Score**: Sorts results by Reddit post score (upvotes minus downvotes).
- **Time**: Sorts results by post recency (most recent first).
- **Combined**: Custom ranking that combines relevance, score, and recency using user-defined weights. This is implemented using Elasticsearch's `function_score` query, allowing fine-tuned control over how much each factor influences the final ranking.

### 2. PageRank-Inspired Re-Ranking

A unique feature is the PageRank-inspired re-ranking algorithm:

- **Purpose**: To further refine the ranking by considering both the number of comments (as a proxy for 'links' or engagement) and the post's score (authority).
- **Initialization**: Each post is assigned an initial score based on a weighted combination of the logarithm of its comment count and score.
- **Iteration**: The algorithm iteratively redistributes scores among posts, simulating the way PageRank distributes authority in a network. Posts with similar comment counts reinforce each other's scores, and posts with no outgoing 'links' distribute their score evenly.
- **Result**: After several iterations, posts that are both highly commented and highly upvoted rise to the top, reflecting both popularity and engagement.

### 3. User Interaction

The script provides an interactive CLI for users to:

- Enter search queries
- Select ranking methods and set weights for combined ranking
- Optionally apply the PageRank-inspired re-ranking to any result set
- View detailed results, including Elasticsearch scores and PageRank scores if used

### 4. Customization

- The ranking method and weights can be customized at runtime.
- The PageRank-inspired algorithm can be toggled on or off for any search.

### Summary Table

| Method    | Description                                                       |
| --------- | ----------------------------------------------------------------- |
| relevance | Default Elasticsearch text relevance (BM25)                       |
| score     | Sort by Reddit post score (votes)                                 |
| time      | Sort by post recency                                              |
| combined  | Weighted combination of relevance, score, and recency             |
| PageRank  | Optional re-ranking based on comment count and score (engagement) |

This design allows for highly flexible, explainable, and powerful search over Reddit data, supporting both standard IR techniques and network-inspired ranking.

## Features

- **Flexible Search Queries**: Supports full-text search across all indexed fields.
- **Multiple Ranking Methods**:
  - **Relevance**: Utilizes Elasticsearch's default relevance scoring.
  - **Score**: Ranks results by the number of upvotes (score) in descending order.
  - **Time**: Ranks results by recency, showing the newest posts first.
  - **Combined**: A customizable ranking that blends relevance, Reddit score, and recency with user-defined weights.
- **PageRank-inspired Re-ranking**: Enhances search results by applying a simplified PageRank algorithm. This re-ranks posts based on their "importance," considering the number of comments (as "links") and their overall score, giving more prominence to highly engaged and authoritative posts.
- **Command-Line Interface**: An interactive command-line interface for easy searching and parameter adjustment.

---

## Algorithms and Design

### Elasticsearch Integration

The core of this search engine relies on **Elasticsearch**, a powerful open-source search and analytics engine.

- **Indexing**: It's assumed that Reddit sports data is already indexed in an Elasticsearch index (default: `reddit_sports_data`). Each document in the index represents a Reddit post and contains metadata such as title, subreddit, score, number of comments, and post time.
- **Querying**: The `search_documents` function constructs Elasticsearch queries based on user input. It uses `query_string` for basic full-text search.

### Ranking Methods

#### 1. Relevance

When `sort_method` is "relevance", Elasticsearch's default TF-IDF (Term Frequency-Inverse Document Frequency) or BM25 (Okapi BM25) algorithm is used to determine how relevant a document is to the search query. This is a standard and effective method for text-based search.

#### 2. Score

If `sort_method` is "score", the results are sorted directly by the `metadata.score` field in descending order. This prioritizes posts with the highest number of upvotes.

#### 3. Time

For `sort_method` "time", results are sorted by the `metadata.time` field in descending order, ensuring that the most recent posts appear first.

#### 4. Combined Ranking

The "combined" ranking method utilizes Elasticsearch's **`function_score` query**. This powerful feature allows for custom scoring logic by combining the base relevance score with one or more functions.

- **`field_value_factor` for Score**: The `metadata.score` field is used with a `log1p` modifier. `log1p(x)` calculates `log(1+x)`, which helps to reduce the impact of extremely high scores and provides a more gradual boost based on upvotes. The `weight_score` parameter allows the user to control the influence of this factor.
- **`gauss` function for Time**: A `gauss` (Gaussian) decay function is applied to the `metadata.time` field. This function provides a "recency boost," meaning posts closer to the current date receive a higher score.
  - `scale`: "30d" means the score will decay over 30 days.
  - `offset`: "7d" means posts within the last 7 days will receive the full boost before decay starts.
  - `decay`: 0.5 means the score will be half the maximum at the `scale` distance from the origin (current time + offset).
  - The `weight_time` parameter controls the influence of this recency boost.
- **`boost_mode: multiply` and `score_mode: sum`**: These parameters determine how the function scores are combined with the base relevance score. In this implementation, the `boost_mode` is set to "multiply" (the base score is multiplied by the function scores) and `score_mode` is set to "sum" (the individual function scores are summed before multiplication).

### PageRank-inspired Algorithm (`calculate_pagerank_score`)

This function implements a simplified, iterative algorithm inspired by Google's PageRank. Its goal is to identify "important" or "authoritative" posts within the search results.

- **Simplified Model**: Unlike traditional PageRank which analyzes a graph of hyperlinks, this model adapts the concept for Reddit posts:
  - **"Links"**: The number of comments (`num_comments`) is treated as a proxy for "incoming links." Posts with more comments are considered more "linked to" or discussed.
  - **"Authority"**: The post's `score` (upvotes) is used as an indicator of its intrinsic authority or quality.
- **Initial Score Calculation**: Each post is assigned an initial score based on a weighted combination of `log1p(num_comments)` and `log1p(score)`. The `log1p` transformation helps to normalize the values and prevent outliers from dominating the initial scores.
- **Normalization**: Initial scores are normalized so their sum is 1, distributing the "ranking power" across all posts.
- **Iterative Refinement**: The core of the algorithm runs for a fixed number of iterations (default 10). In each iteration:
  - **Damping Factor**: A `damping_factor` (default 0.85) is applied, similar to traditional PageRank, representing the probability that a "random surfer" will continue clicking links rather than jumping to a random page.
  - **Score Distribution**: Each post distributes its current score to other posts based on a **similarity heuristic** related to comment count. The more similar two posts are in terms of comment count, the more "link strength" is assumed between them.
  - **Handling No Outgoing Links**: A small safeguard ensures that if a post has no "outgoing links" (e.g., no comments or very low comment similarity with others), its score is distributed evenly among other posts to prevent "rank sinks."
- **Re-ranking**: If `use_pagerank` is true, the `search_documents` function first retrieves results from Elasticsearch using the chosen `sort_method`. Then, it calculates PageRank scores for _these retrieved results_ and re-sorts them based on their PageRank scores. This means PageRank acts as a secondary re-ranking layer on top of the initial Elasticsearch search.

---

## Setup and Installation

1.  **Elasticsearch**: Ensure you have an Elasticsearch instance running. You can set its URL via the `ELASTICSEARCH_URL` environment variable. If not set, it defaults to `http://localhost:9200`.
2.  **Python Dependencies**: Install the required Python libraries:
    ```bash
    pip install elasticsearch numpy
    ```
3.  **Environment Variables**:

    - `ELASTICSEARCH_URL`: (Optional) Set this to your Elasticsearch instance URL (e.g., `http://localhost:9200`).
    - `ES_INDEX_NAME`: (Optional) Set this to the name of your Elasticsearch index containing Reddit sports data (defaults to `reddit_sports_data`).

    Example:

    ```bash
    export ELASTICSEARCH_URL="http://localhost:9200"
    export ES_INDEX_NAME="reddit_sports_data"
    ```

---

## Usage

To run the search engine, execute the Python script:

```bash
python search_index.py
```

To get API's, execute the Python script:

```bash
python main.py
```
