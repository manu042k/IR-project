import os
import re
from collections import defaultdict
from urllib.parse import urlparse


def read_seed_file(seed_file_path):
    """
    Reads a seed file with categories and associated URLs or subreddit names.

    The file format expected is:
    #CategoryName1
    http://url1.com
    https://www.reddit.com/r/SubredditName1/
    #CategoryName2
    http://url3.com
    https://www.reddit.com/r/SubredditName2/
    ...

    If a URL matches the pattern 'https://www.reddit.com/r/SubredditName/',
    only 'SubredditName' is added to the list for that category.

    Args:
        seed_file_path (str): The path to the seed file.

    Returns:
        dict: A dictionary where keys are category names (str)
              and values are lists of URLs or subreddit names (str)
              belonging to that category.
              Returns an empty dictionary if the file doesn't exist or
              an error occurs.
    """
    # Pattern to match reddit subreddit URLs
    REDDIT_PATTERN = r'^https://(?:www\.)?reddit\.com/r/([^/]+)/?$'
    
    category_links = defaultdict(list)
    current_category = None

    # Check if the seed file exists
    if not os.path.exists(seed_file_path):
        print(f"Error: Seed file not found at {seed_file_path}")
        return {}  # Return empty dict if file not found

    try:
        with open(seed_file_path, 'r') as f:
            for line_number, line in enumerate(f, 1):
                line = line.strip()  # Remove leading/trailing whitespace and newlines
                
                if not line:
                    continue  # Skip empty lines

                if line.startswith('#'):
                    # Found a new category
                    current_category = line[1:].strip()
                elif current_category is not None:
                    # Process URL or subreddit name
                    _process_seed_line(line, current_category, category_links, REDDIT_PATTERN, line_number)
                else:
                    # Line doesn't start with # and no category is active yet
                    print(f"Warning: Line {line_number}: Skipping line outside of any category: {line}")

    except Exception as e:
        print(f"Error reading seed file {seed_file_path}: {e}")
        return {}  # Return empty dict on error

    # Convert defaultdict back to a regular dict for the return value
    return dict(category_links)


def _process_seed_line(line, category, category_links, reddit_pattern, line_number):
    """
    Process a single line from the seed file.
    
    Args:
        line (str): The line to process
        category (str): The current category
        category_links (defaultdict): Dictionary to store links by category
        reddit_pattern (str): Regex pattern to match Reddit URLs
        line_number (int): Current line number for error reporting
    """
    # Check if it's a Reddit subreddit URL
    match = re.match(reddit_pattern, line, re.IGNORECASE)
    
    if match:
        subreddit_name = match.group(1)
        category_links[category].append(subreddit_name)
    # Basic validation: check if it looks like a URL
    elif line.startswith('http://') or line.startswith('https://'):
        category_links[category].append(line)
    else:
        print(f"Warning: Line {line_number}: Skipping line, does not look like a valid URL under category '{category}': {line}")
