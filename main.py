import dotenv
import pandas as pd
import os
from urllib.parse import urlparse
from crawler.init_crawler import initalize_reddit
from utils.read_seed import read_seed_file
from crawler.extract_posts import get_posts
from utils.save_posts import save_posts

# Load environment variables from .env file
dotenv.load_dotenv()

# import the root url from the environment variable
root_url = os.getenv("ROOT_URL")
reddit_read_only = initalize_reddit()

# From seed file, read urls and extract the subreddit names
# Define the path to the seed file
seed_file_path = 'seed.txt' # Assuming the file is in the same directory

subreddit_names = read_seed_file(seed_file_path)

if not subreddit_names:
	print("No subreddits found or extracted. Exiting.")
	exit() # Or handle this case as needed

posts_list, count = get_posts(root_url, reddit_read_only, subreddit_names)

# Save the posts to a CSV file
save_posts(posts_list, option="json")

	


