import praw
import os
from dotenv import load_dotenv


def initialize_reddit():
    """
    Initialize and return a read-only Reddit PRAW instance.
    
    This function creates a connection to the Reddit API using PRAW.
    In a production environment, credentials should be loaded from
    environment variables or a config file.
    
    Returns:
        praw.Reddit: A read-only Reddit instance
    """
    # In production, use environment variables instead of hardcoded credentials
    # load_dotenv()  # Uncomment to use .env file for credentials
    # client_id = os.getenv("REDDIT_CLIENT_ID")
    # client_secret = os.getenv("REDDIT_CLIENT_SECRET")
    
    reddit_read_only = praw.Reddit(
        client_id="_joGaqGb9XUDk47Fy4srhw",      # your client id
        client_secret="UFK8WPrlSWUJpcKBgg-wkfxzsxqRcg",  # your client secret
        user_agent="ir_project",                # your user agent
        ratelimit_seconds=15                    # your rate limit
    )
    return reddit_read_only