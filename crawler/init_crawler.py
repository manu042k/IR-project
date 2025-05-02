import praw


def initalize_reddit():
    reddit_read_only = praw.Reddit(client_id="_joGaqGb9XUDk47Fy4srhw",		 # your client id
							client_secret="UFK8WPrlSWUJpcKBgg-wkfxzsxqRcg",	 # your client secret
							user_agent="ir_project",         # your user agent
							ratelimit_seconds=15)	 # your rate limit	
    return reddit_read_only