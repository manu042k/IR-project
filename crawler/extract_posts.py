from utils.get_subreddit import get_info
import time
import matplotlib.pyplot as plt
import concurrent.futures
import threading


def get_posts(root_url, reddit_read_only, subreddit_names, max_workers=5):
    """
    Scrape posts from multiple subreddits and track the scraping time.
    
    Args:
        root_url (str): Base URL for Reddit
        reddit_read_only: PRAW Reddit instance for read-only operations
        subreddit_names (dict): Dictionary mapping categories to list of subreddit names
        max_workers (int): Maximum number of worker threads to use
        
    Returns:
        tuple: (list of post dictionaries, total number of posts scraped)
    """
    posts_list = []
    total_post_count = 0
    time_stamp = {0: 0}
    time_start = time.time()
    
    # Create locks for thread-safe operations
    posts_lock = threading.Lock()
    count_lock = threading.Lock()
    time_lock = threading.Lock()
    
    # Process subreddits using thread pool
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Create a list to store all futures
        futures = []
        
        for category, subreddits in subreddit_names.items():
            print("###############################")
            print(f"Category: {category}")
            
            for subreddit_name in subreddits:
                # Submit each subreddit processing task to the thread pool
                future = executor.submit(
                    _process_subreddit_threaded,
                    root_url, 
                    reddit_read_only, 
                    subreddit_name, 
                    category, 
                    posts_list,
                    posts_lock,
                    total_post_count,
                    count_lock,
                    time_start, 
                    time_stamp,
                    time_lock
                )
                futures.append((future, subreddit_name))
        
        # Process results as they complete
        for future, subreddit_name in futures:
            try:
                subreddit_post_count = future.result()
                
                with count_lock:
                    total_post_count += subreddit_post_count
                
                print("*********************************")
                print(f"Subreddit Name: {subreddit_name}")
                print(f"Total Posts Scraped from Subreddit: {subreddit_post_count}")
                
            except Exception as e:
                print(f"Error fetching posts from subreddit {subreddit_name}: {e}")
    
    _plot_scraping_performance(time_stamp)
    
    return posts_list, total_post_count


def _process_subreddit_threaded(root_url, reddit_read_only, subreddit_name, category, 
                               posts_list, posts_lock, current_total_count, count_lock,
                               time_start, time_stamp, time_lock):
    """
    Thread-safe version of _process_subreddit that processes a single subreddit.
    
    Args:
        root_url (str): Base URL for Reddit
        reddit_read_only: PRAW Reddit instance
        subreddit_name (str): Name of the subreddit to process
        category (str): Category the subreddit belongs to
        posts_list (list): Shared list to store all posts
        posts_lock (threading.Lock): Lock for thread-safe list updates
        current_total_count (int): Current total post count
        count_lock (threading.Lock): Lock for thread-safe count updates
        time_start (float): Start time of the scraping process
        time_stamp (dict): Dictionary to track scraping progress
        time_lock (threading.Lock): Lock for thread-safe timestamp updates
        
    Returns:
        int: Count of posts from this subreddit
    """
    posts_from_subreddit = []
    subreddit_post_count = 0
    
    try:
        # Create subreddit instance
        subreddit = reddit_read_only.subreddit(subreddit_name)
        
        # Get subreddit information
        name, title, subscribers, description = get_info(reddit_read_only, subreddit_name)
        
        # Get different types of posts
        post_listings = _get_post_listings(subreddit)
        
        # Process each post listing
        for post_listing in post_listings:
            for post in post_listing:
                post_obj = {
                    "Subreddit": subreddit.display_name,
                    "Subreddit URL": root_url + subreddit.url,
                    "Title": post.title,
                    "Post Text": post.selftext,
                    "ID": post.id,
                    "Score": post.score,
                    "Total Comments": post.num_comments,
                    "Post URL": post.url,
                    "Sports category": category,
                }
                
                posts_from_subreddit.append(post_obj)
                subreddit_post_count += 1
                
                
        
        # Thread-safe update of the global posts list
        with posts_lock:
            posts_list.extend(posts_from_subreddit)
            with time_lock:
                time_stamp[len(posts_list)] = time.time() - time_start
        
        print(time_stamp)
        return subreddit_post_count
    
    except Exception as e:
        print(f"Error processing subreddit {subreddit_name}: {e}")
        return 0


def _process_subreddit(root_url, reddit_read_only, subreddit_name, category, current_count, time_start, time_stamp):
    """
    Process a single subreddit to extract all relevant posts.
    
    Args:
        root_url (str): Base URL for Reddit
        reddit_read_only: PRAW Reddit instance
        subreddit_name (str): Name of the subreddit to process
        category (str): Category the subreddit belongs to
        current_count (int): Current total post count
        time_start (float): Start time of the scraping process
        time_stamp (dict): Dictionary to track scraping progress
        
    Returns:
        tuple: (list of posts from this subreddit, count of posts from this subreddit)
    """
    posts_from_subreddit = []
    subreddit_post_count = 0
    
    # Create subreddit instance
    subreddit = reddit_read_only.subreddit(subreddit_name)
    
    # Get subreddit information
    name, title, subscribers, description = get_info(reddit_read_only, subreddit_name)
    
    # Get different types of posts
    post_listings = _get_post_listings(subreddit)
    
    # Process each post listing
    for post_listing in post_listings:
        for post in post_listing:
            post_obj = {
                "Subreddit": subreddit.display_name,
                "Subreddit URL": root_url + subreddit.url,
                "Title": post.title,
                "Post Text": post.selftext,
                "ID": post.id,
                "Score": post.score,
                "Total Comments": post.num_comments,
                "Post URL": post.url,
                "Sports category": category,
            }
            
            posts_from_subreddit.append(post_obj)
            subreddit_post_count += 1
            current_count += 1
            
            # Record timestamp at regular intervals
            
            time_stamp[current_count] = time.time() - time_start    
    return posts_from_subreddit, subreddit_post_count


def _get_post_listings(subreddit):
    """
    Get different types of post listings from a subreddit.
    
    Args:
        subreddit: PRAW Subreddit instance
        
    Returns:
        list: List of post listing iterators
    """
    return [
        subreddit.top(time_filter="all", limit=None),
        subreddit.hot(limit=None),
        subreddit.new(limit=None),
        subreddit.rising(limit=None),
        subreddit.controversial(limit=None),
    ]


def _plot_scraping_performance(time_stamp):
    """
    Plot and save a graph showing scraping performance over time.
    Reduces the number of points plotted by sampling the data.
    
    Args:
        time_stamp (dict): Dictionary mapping post counts to elapsed time
    """
    if not time_stamp:
        return
        
    plt.figure(figsize=(10, 6))
    
    # Extract x and y values
    x_values = list(time_stamp.keys())
    y_values = list(time_stamp.values())
    
    plt.plot(x_values, y_values, linestyle='-')
    plt.title('Time Taken to Scrape Posts')
    plt.xlabel('Number of Posts')
    plt.ylabel('Time (seconds)')
    
    plt.grid(True)
    plt.savefig('scraping_time.png')
    plt.close()
    print(f"Graph saved as scraping_time.png (Showing  data points)")
