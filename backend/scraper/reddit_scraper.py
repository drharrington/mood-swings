import praw
import logging
from backend.scraper.scraper_utils import process_data, save_to_csv

from backend.config import (
    REDDIT_USERNAME,
    REDDIT_PASSWORD,
    CLIENT_ID,
    CLIENT_SECRET,
    USER_AGENT,
)

logger = logging.getLogger(__name__)

DEFAULT_MAX_POSTS = 30
DEFAULT_MAX_COMMENTS = 10

def fetch_brand_data(brand_name, max_posts=DEFAULT_MAX_POSTS, max_comments=DEFAULT_MAX_COMMENTS, reddit_client=None):
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
            brand_name, limit=max_posts, sort="top"
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

            # Fetch top-level comments, limited to max_comments
            submission.comment_sort = "top"
            submission.comments.replace_more(
                limit=0
            )
            top_comments = submission.comments.list()[:max_comments]  # Limit comments
            for top_comment in top_comments:
                post_data["comments"].append(
                    {"id": top_comment.id, "body": top_comment.body, "score": top_comment.score}
                )

            data.append(post_data)
    except praw.exceptions.APIException as e:
        logging.error(f"Reddit API error: {e}")
    except praw.exceptions.ClientException as e:
        logging.error(f"Reddit client error: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
    return data


def run_scraper(brand_name, max_posts=10, max_comments=5, reddit_client=None):
    """Fetch Reddit data for a brand and save it to CSV."""
    try:
        logging.info(f"Fetching data for brand: {brand_name} with max_posts = {max_posts} and max_comments = {max_comments}")
        reddit_data = fetch_brand_data(brand_name, max_posts, max_comments, reddit_client)
        posts, comments = process_data(reddit_data, brand_name)
        save_to_csv(posts, comments)
        logging.info("Scraping completed successfully.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    run_scraper()
