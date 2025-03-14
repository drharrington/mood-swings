import praw
from config import REDDIT_USERNAME, REDDIT_PASSWORD, CLIENT_ID, CLIENT_SECRET, USER_AGENT

# Function to fetch Reddit posts about a specific brand
def fetch_brand_posts(brand_name):
    # Initialize Reddit API client
    reddit = praw.Reddit(
        username=REDDIT_USERNAME,
        password=REDDIT_PASSWORD,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        user_agent=USER_AGENT
    )

    # Search for posts mentioning the brand in the title or body
    print(f"Searching for posts about '{brand_name}'...")

    # You can customize the search query and add more filters (e.g., sort by top or new)
    for submission in reddit.subreddit('all').search(brand_name, limit=5, sort='top'):
        print(f"Title: {submission.title}")
        print(f"URL: {submission.url}")
        print(f"Score: {submission.score}")
        print(f"ID: {submission.id}")
        print(f"Subreddit: {submission.subreddit.display_name}")
        print("-" * 30)

        # Fetch the comments if needed
        submission.comments.replace_more(limit=5)  # Remove "load more comments" links
        for comment in submission.comments.list():
            if brand_name.lower() in comment.body.lower():
                print(f"Comment by {comment.author}: {comment.body}")
                print("-" * 30)

# Example: User specifies the brand they want to search for
brand_name = input("Enter the brand name to search for: ")
fetch_brand_posts(brand_name)
