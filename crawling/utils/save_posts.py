import pandas as pd
import os
import json
from pathlib import Path


def save_posts(posts_list, option="json", output_directory=""):
    """
    Save the scraped posts to a file in the specified format.
    
    Args:
        posts_list (list): List of dictionaries containing post data
        option (str): File format to save data in ('json' or 'csv')
        output_directory (str): Directory to save the output file (optional)
        
    Returns:
        str: Path to the saved file, or None if there was an error
    """
    if not posts_list:
        print("Warning: No posts to save")
        return None
        
    # Create output directory if it doesn't exist and a directory was specified
    if output_directory and not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    # Convert to dataframe for easier manipulation
    df = pd.DataFrame(posts_list)
    
    # Construct the output path
    base_filename = "posts"
    output_path = os.path.join(output_directory, f"{base_filename}.{option}")
    
    try:
        if option.lower() == "csv":
            df.to_csv(output_path, index=False)
        elif option.lower() == "json":
            df.to_json(output_path, orient="records", indent=4)
        else:
            print(f"Error: Invalid output format '{option}'. Please choose 'csv' or 'json'.")
            return None
            
        print(f"Posts saved to {output_path}")
        print(f"Total Posts Saved: {len(posts_list)}")
        
        return output_path
        
    except Exception as e:
        print(f"Error saving posts: {e}")
        return None
