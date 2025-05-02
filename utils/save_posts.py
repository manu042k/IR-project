import pandas as pd
import os
from urllib.parse import urlparse
import numpy as np

def save_posts(posts_list, option="csv"):
    if option == "csv":
        df = pd.DataFrame(posts_list)
        df.to_csv('posts.csv', index=False)
        print("Posts saved to posts.csv")
        print("Total Posts Scraped: ", len(posts_list))

    if option == "json":
        df = pd.DataFrame(posts_list)
        df.to_json('posts.json', orient="records", lines=True)
        print("Posts saved to posts.json")
        print("Total Posts Scraped: ", len(posts_list))
    
    else: 
        print("Invalid option. Please choose 'csv' or 'json'.")
        return None
