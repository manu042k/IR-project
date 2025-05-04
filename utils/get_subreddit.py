import praw


def get_info(reddit_instance, subreddit_name):
    """
    Get basic information about a subreddit.
    
    Args:
        reddit_instance: PRAW Reddit instance
        subreddit_name (str): Name of the subreddit
        
    Returns:
        tuple: (display_name, title, subscribers_count, description)
        
    Raises:
        praw.exceptions.PRAWException: If there's an error retrieving subreddit data
    """
    try:
        subreddit = reddit_instance.subreddit(subreddit_name)
        name = subreddit.display_name
        title = subreddit.title
        subscribers = subreddit.subscribers
        description = subreddit.description
        return name, title, subscribers, description
    except Exception as e:
        print(f"Error retrieving information for subreddit {subreddit_name}: {e}")
        # Return default values in case of error
        return subreddit_name, "", 0, ""


