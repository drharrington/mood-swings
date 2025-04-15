import os
import re
import pandas as pd
import logging


def clean_text(text):
    """Clean text by removing URLs, special characters, punctuation, and extra spaces."""
    # Remove URLs (including those without http/https/www)
    text = re.sub(
        r"\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b", "", text
    )  # Matches domain-like patterns
    text = re.sub(
        r"http\S+|www\S+", "", text, flags=re.MULTILINE
    )  # Matches http/https/www URLs
    # Remove special characters and punctuation
    text = re.sub(r"[^\w\s]", "", text)  # Keep only words and spaces
    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)  # Replace multiple spaces with a single space
    return text.strip().lower()


def process_data(data, brand_name):
    """Process raw Reddit data into separate lists for posts and comments."""
    posts = []
    comments = []
    for post in data:
        posts.append(
            {
                "brand_name": brand_name,
                "post_id": post["id"],
                "post_title": clean_text(post["title"]),
                "post_body": clean_text(post["selftext"]),
                "post_score": post["score"],
                "post_url": post["url"],
                "post_num_comments": post["num_comments"],
                "timestamp": post.get("created_utc", "N/A"),
            }
        )
        for comment in post["comments"]:
            comments.append(
                {
                    "brand_name": brand_name,
                    "post_id": post["id"],
                    "comment_id": comment["id"],
                    "comment_body": clean_text(
                        comment["body"]
                        if comment["body"] not in ["[deleted]", "[removed]"]
                        else "Deleted Comment"
                    ),
                    "comment_score": comment["score"],
                }
            )
    return posts, comments


def save_to_csv(
    posts, comments, posts_filename="posts.csv", comments_filename="comments.csv"
):
    """Save posts and comments to separate CSV files in the data directory."""
    try:
        data_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data"
        )
        os.makedirs(data_dir, exist_ok=True)

        posts_file_path = os.path.join(data_dir, posts_filename)
        pd.DataFrame(posts).to_csv(posts_file_path, index=False, encoding="utf-8")
        logging.info(f"Raw posts data saved to {posts_file_path}")

        comments_file_path = os.path.join(data_dir, comments_filename)
        pd.DataFrame(comments).to_csv(comments_file_path, index=False, encoding="utf-8")
        logging.info(f"Comments data saved to {comments_file_path}")
    except Exception as e:
        logging.error(f"Error saving data to CSV: {e}")
