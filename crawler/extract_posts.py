from utils.get_subreddit import get_info

def get_posts(root_url, reddit_read_only, subreddit_names):
	posts_list = []
	count = 0

	for subr in subreddit_names:
		subr_count = 0
		# Creating a Reddit instance
		subreddit = reddit_read_only.subreddit(subr)
		
        # Getting subreddit information
		name, title, subscribers, description = get_info(reddit_read_only, subr)
		print("Subreddit Name: ", name)

		top_posts = subreddit.top(time_filter = "all", limit = None) 
		hot_posts = subreddit.hot(limit = None)
		new_posts = subreddit.new(limit = None)
		rising_posts = subreddit.rising(limit = None)
		controversial_posts = subreddit.controversial(limit = None)
		posts = [top_posts, hot_posts, new_posts, rising_posts, controversial_posts]
		c = 0
		for type_post in posts:
			for post in type_post:
				
				post_obj = {
					"Subreddit": subreddit.display_name,
					"Subreddit URL": root_url + subreddit.url,
					"Title": post.title,
					"Post Text": post.selftext,
					"ID": post.id,
					"Score": post.score,
					"Total Comments": post.num_comments,
					"Post URL": post.url,
				}
				# Append the post object to the posts list
				posts_list.append(post_obj)
				count += 1
				subr_count += 1
		print("Total Posts Scraped from Subreddit: ", subr_count)
		print()

	return posts_list, count
