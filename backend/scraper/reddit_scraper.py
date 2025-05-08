import praw
import pandas as pd
import logging
from backend.scraper.scraper_utils import process_data, save_to_csv

from backend.config import (
    REDDIT_USERNAME,
    REDDIT_PASSWORD,
    CLIENT_ID,
    CLIENT_SECRET,
    USER_AGENT,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def fetch_brand_data(brand_name, limit=10, reddit_client=None):
    """Fetch Reddit posts about a specific brand."""

    # Initialize Reddit API client
    reddit_client = reddit_client or praw.Reddit(
        username=REDDIT_USERNAME,
        password=REDDIT_PASSWORD,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        user_agent=USER_AGENT,
    )

    data = []
    try:
        # Search for posts mentioning the brand in the title or body
        for submission in reddit_client.subreddit("all").search(
            brand_name, limit=limit, sort="top"
        ):
            post_data = {
                "id": submission.id,
                "title": submission.title,
                "selftext": submission.selftext,
                "score": submission.score,
                "url": submission.url,
                "num_comments": submission.num_comments,
                "comments": [],
            }

            submission.comments.replace_more(
                limit=5
            )  # Get top-level comments, up to 5 layers deep
            for comment in submission.comments.list():
                post_data["comments"].append(
                    {"id": comment.id, "body": comment.body, "score": comment.score}
                )

            data.append(post_data)
    except Exception as e:
        logging.error(f"Error fetching data from Reddit: {e}")
    return data


if __name__ == "__main__":
    try:
        brand_name = input("Enter brand name: ").strip()
        if not brand_name:
            raise ValueError("Brand name cannot be empty.")
        limit = int(input("Enter the number of posts to fetch (default 10): ") or 10)
        logging.info(f"Fetching data for brand: {brand_name} with limit: {limit}")
        reddit_data = fetch_brand_data(brand_name, limit=limit)
        posts, comments = process_data(reddit_data, brand_name)
        save_to_csv(posts, comments)
    except ValueError as ve:
        logging.error(f"Input error: {ve}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
