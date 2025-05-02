import praw

def get_info(reddit_instance, subreddit_name):
    subreddit = reddit_instance.subreddit(subreddit_name)
    name = subreddit.display_name
    title = subreddit.title
    subscribers = subreddit.subscribers
    description = subreddit.description
    return name, title, subscribers, description


