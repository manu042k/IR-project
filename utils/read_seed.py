import os
from urllib.parse import urlparse

def read_seed_file(seed_file_path):
	subreddit_names = []
	# Check if the seed file exists
	if os.path.exists(seed_file_path):
		try:
			with open(seed_file_path, 'r') as f:
				urls = f.readlines()

			for url in urls:
				url = url.strip() # Remove leading/trailing whitespace and newlines
				if not url:
					continue # Skip empty lines

				try:
					parsed_url = urlparse(url)
					# Expected path format: /r/subreddit_name/...
					path_parts = parsed_url.path.strip('/').split('/')
					if len(path_parts) >= 2 and path_parts[0].lower() == 'r':
						subreddit_name = path_parts[1]
						if subreddit_name not in subreddit_names:
							subreddit_names.append(subreddit_name)
					else:
						print(f"Warning: Could not extract subreddit from URL: {url}")
				except Exception as e:
					print(f"Warning: Error parsing URL {url}: {e}")

		except FileNotFoundError:
			print(f"Error: Seed file not found at {seed_file_path}")
		except Exception as e:
			print(f"Error reading seed file {seed_file_path}: {e}")
	else:
		print(f"Warning: Seed file {seed_file_path} does not exist. Using default subreddit.")
		# Optionally, add a default subreddit if the file doesn't exist
		# subreddit_names.append("redditdev") # Example default

	# Print the extracted subreddit names (optional)
	print("Extracted Subreddit Names:", subreddit_names)
	return subreddit_names