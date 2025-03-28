import praw
import sys
import os
import pandas as pd
import logging
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.config import REDDIT_USERNAME, REDDIT_PASSWORD, CLIENT_ID, CLIENT_SECRET, USER_AGENT

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Initialize Reddit API client
reddit = praw.Reddit(
        username=REDDIT_USERNAME,
        password=REDDIT_PASSWORD,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        user_agent=USER_AGENT
    )

def fetch_brand_data(brand_name, limit=10):
    """Fetch Reddit posts about a specific brand."""
    data = []
    try:
        # Search for posts mentioning the brand in the title or body
        for submission in reddit.subreddit('all').search(brand_name, limit=limit, sort='top'):
            post_data = {
                "id": submission.id,
                "title": submission.title,
                "selftext": submission.selftext,
                "score": submission.score,
                "url": submission.url,
                "num_comments": submission.num_comments,
                "comments": []
            }

            submission.comments.replace_more(limit=5)  # Get top-level comments, up to 5 layers deep
            for comment in submission.comments.list():
                post_data["comments"].append({
                    "id": comment.id,
                    "body": comment.body,
                    "score": comment.score
                })

            data.append(post_data)
    except Exception as e:
        logging.error(f"Error fetching data from Reddit: {e}")
    return data

def process_data(data, brand_name):
    """Process raw Reddit data into separate lists for posts and comments."""
    posts = []
    comments = []
    for post in data:
        # Add post data
        posts.append({
"brand_name": brand_name,  # Add brand name
                "post_id": post["id"],
                "post_title": post["title"],
                "post_body": post["selftext"],
                "post_score": post["score"],
                "post_url": post["url"],
                "post_num_comments": post["num_comments"],
"timestamp": post.get("created_utc", "N/A")  # Handle missing timestamps
        })
        # Add comment data
        for comment in post["comments"]:
            comments.append({
"brand_name": brand_name,  # Add brand name
                "post_id": post["id"],
                "comment_id": comment["id"],
                "comment_body": comment["body"] if comment["body"] not in ["[deleted]", "[removed]"] else "Deleted Comment",  # Handle deleted comments
                "comment_score": comment["score"]
            })
    return posts, comments

def save_to_csv(posts, comments, posts_filename="posts.csv", comments_filename="comments.csv"):
    """Save posts and comments to separate CSV files in the data directory."""
    try:
        # Ensure the data directory exists
        data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
        os.makedirs(data_dir, exist_ok=True)

        # Save raw posts to posts.csv
        posts_file_path = os.path.join(data_dir, posts_filename)
        pd.DataFrame(posts).to_csv(posts_file_path, index=False, encoding="utf-8")
        logging.info(f"Raw posts data saved to {posts_file_path}")

        # Save raw comments to comments.csv
        comments_file_path = os.path.join(data_dir, comments_filename)
        pd.DataFrame(comments).to_csv(comments_file_path, index=False, encoding="utf-8")
        logging.info(f"Comments data saved to {comments_file_path}")
    except Exception as e:
        logging.error(f"Error saving data to CSV: {e}")

if __name__ == "__main__":
    try:
        brand_name = input("Enter brand name: ").strip()  # Get brand input from user
        if not brand_name:
            raise ValueError("Brand name cannot be empty.")
        limit = int(input("Enter the number of posts to fetch (default 10): ") or 10)  # Allow user to specify limit
        logging.info(f"Fetching data for brand: {brand_name} with limit: {limit}")
        reddit_data = fetch_brand_data(brand_name, limit=limit)
        posts, comments = process_data(reddit_data, brand_name)
        save_to_csv(posts, comments)
    except ValueError as ve:
        logging.error(f"Input error: {ve}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")