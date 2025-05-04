#!/usr/bin/env python3
"""
Reddit Post Crawler

This script crawls Reddit for posts from specified subreddits defined in a seed file,
processes them, and saves the collected data in JSON format.
"""

import os
import dotenv
import pandas as pd
from urllib.parse import urlparse

from crawler.init_crawler import initialize_reddit
from utils.read_seed import read_seed_file
from crawler.extract_posts import get_posts
from utils.save_posts import save_posts


def main():
    """
    Main function to orchestrate the Reddit post crawling process.
    """
    # Load environment variables
    dotenv.load_dotenv()
    
    # Get configuration
    root_url = os.getenv("ROOT_URL", "https://www.reddit.com")
    seed_file_path = os.getenv("SEED_FILE", "seed.txt")
    output_format = os.getenv("OUTPUT_FORMAT", "json")
    
    # Initialize Reddit client
    reddit_client = initialize_reddit()
    
    # Read subreddit categories and names from seed file
    subreddit_categories = read_seed_file(seed_file_path)
    if not subreddit_categories:
        print("Error: No subreddits found in the seed file. Exiting.")
        return 1
        
    print(f"Found {sum(len(subs) for subs in subreddit_categories.values())} subreddits in {len(subreddit_categories)} categories")
    
    # Extract posts from subreddits
    posts_data, post_count = get_posts(root_url, reddit_client, subreddit_categories)
    print(f"Successfully scraped {post_count} posts from Reddit")
    
    # Save the posts data
    output_path = save_posts(posts_data, option=output_format)
    print(f"Data saved to {output_path}")
    
    return 0


if __name__ == "__main__":
    exit(main())




