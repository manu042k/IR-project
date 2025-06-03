# Reddit Post Crawler

A Python tool for crawling Reddit posts from specified subreddits, processing them, and saving the collected data in JSON or CSV format.

## Project Overview

This project is designed to extract posts from various subreddits categorized by sports/topics. It uses the PRAW (Python Reddit API Wrapper) library to access Reddit's API and collect posts from the specified subreddits. The collected data is then processed and saved in the desired format (JSON or CSV).

## Features

- Extracts posts from multiple subreddits in parallel using multithreading
- Organizes subreddits by categories
- Collects different types of posts (top, hot, new, rising, controversial)
- Tracks scraping performance with time visualization
- Saves data in JSON or CSV format
- Configurable through environment variables

## Project Structure

```
.
├── crawler/
│   ├── extract_posts.py       # Functions to extract posts from subreddits
│   └── init_crawler.py        # Initialize Reddit API client
├── utils/
│   ├── get_subreddit.py       # Utility to get subreddit info
│   ├── read_seed.py           # Functions to read the seed file
│   └── save_posts.py          # Functions to save posts to file
├── env/                       # Virtual environment (not tracked in git)
├── crawler.sh                 # Shell script to automate setup and execution
├── main.py                    # Main script to orchestrate the process
├── requirements.txt           # Project dependencies
├── seed.txt                   # List of subreddits to crawl
├── scraping_time.png          # Performance visualization (generated)
└── README.md                  # This documentation
```

## Prerequisites

- Python 3.6 or higher
- Reddit API credentials (client ID, client secret)
- Required Python packages (see `requirements.txt`)

## Getting Started

1. **Clone the repository**

```bash
git clone <repository-url>
cd IR-project
```

2. **Create and activate a virtual environment (optional but recommended)**

```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

3. **Install required packages**

```bash
pip install -r requirements.txt
```

4. **Set up Reddit API credentials**

Register an application on Reddit to get API credentials:

- Go to https://www.reddit.com/prefs/apps
- Click "create app" at the bottom
- Fill in the required information
- Select "script" for the type of app

Once you have your credentials, you can either:

- Update them directly in `crawler/init_crawler.py`
- Or create a `.env` file in the root directory with:
  ```
  REDDIT_CLIENT_ID=your_client_id
  REDDIT_CLIENT_SECRET=your_client_secret
  ```

## Configuration

The project can be configured using environment variables or the `.env` file:

- `ROOT_URL`: Base URL for Reddit (default: "https://www.reddit.com")
- `SEED_FILE`: Path to the seed file (default: "seed.txt")
- `OUTPUT_FORMAT`: Format to save data in ("json" or "csv") (default: "json")
- `MAX_WORKERS`: Maximum number of worker threads (default: 5)
- `REDDIT_CLIENT_ID`: Your Reddit API client ID
- `REDDIT_CLIENT_SECRET`: Your Reddit API client secret

## Usage

1. **Run the crawler**

```bash
python main.py
```

Alternatively, use the provided shell script to automate setup:

```bash
chmod +x crawler.sh
./crawler.sh
```

The `crawler.sh` script:

- Checks for the virtual environment and creates one if needed
- Activates the virtual environment
- Installs dependencies from `requirements.txt`
- Runs `main.py` with 8 worker threads (`MAX_WORKERS=8`)

This is the recommended method for first-time users as it handles all setup automatically.

2. **Check the output**

Results will be saved as `posts.json` or `posts.csv` depending on your configuration.
A performance graph will be generated as `scraping_time.png` showing the time taken to scrape posts.

## Seed File Format

The seed file (`seed.txt`) contains categories and subreddit URLs in the following format:

```
#CategoryName1
https://www.reddit.com/r/SubredditName1/
https://www.reddit.com/r/SubredditName2/
#CategoryName2
https://www.reddit.com/r/SubredditName3/
https://www.reddit.com/r/SubredditName4/
```

Each category starts with a `#` followed by the category name. Each line after a category and before the next category is treated as a subreddit URL for that category.

## Output Format

The crawler collects the following information for each post:

- Subreddit name
- Subreddit URL
- Post title
- Post text content
- Post ID
- Score (upvotes - downvotes)
- Total comments
- Post URL
- Sports category

## Performance Visualization

The project generates a graph (`scraping_time.png`) that shows the time taken to scrape posts. This can be useful for performance analysis and optimization.

## Limitations

- The Reddit API has rate limits that may affect the speed of data collection
- Very large datasets might require additional memory management
- Private subreddits or quarantined content might not be accessible

## Team Members

- [Manoj Manjunatha](https://github.com/manu042k)
- [Vijay Ram Enaganti](https://github.com/VjayRam)
- [Sanjay Srinivasa](https://github.com/Sanjay1S)
- [Sumukh Balu Somalaram](https://github.com/sumukhbalu84)
- [Lakhan Kumar Sunil Kumar](https://github.com/1629lyk)


