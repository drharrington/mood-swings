import os
import unittest
import logging
from unittest.mock import patch, MagicMock
from backend.scraper.scraper_utils import process_data, save_to_csv
from backend.scraper.reddit_scraper import fetch_brand_data

# Configure logging for the tests
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class TestScraperUtils(unittest.TestCase):
    def setUp(self):
        self.raw_data = [
            {
                "id": "post1",
                "title": "Test Post",
                "selftext": "This is a test post.",
                "score": 100,
                "url": "http://example.com",
                "num_comments": 2,
                "comments": [
                    {"id": "comment1", "body": "Great post!", "score": 10},
                    {"id": "comment2", "body": "[deleted]", "score": 5},
                ],
            }
        ]
        self.brand_name = "TestBrand"
        self.data_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data"
        )

    def test_process_data(self):
        logger.info("Running test_process_data")  # Use logging
        posts, comments = process_data(self.raw_data, self.brand_name)
        self.assertEqual(len(posts), 1)
        self.assertEqual(len(comments), 2)
        self.assertEqual(posts[0]["brand_name"], self.brand_name)
        self.assertEqual(comments[1]["comment_body"], "Deleted Comment")

    def test_save_to_csv(self):
        logger.info("Running test_save_to_csv")  # Use logging
        posts, comments = process_data(self.raw_data, self.brand_name)
        posts_file_path = os.path.join(self.data_dir, "test_posts.csv")
        comments_file_path = os.path.join(self.data_dir, "test_comments.csv")

        save_to_csv(posts, comments, "test_posts.csv", "test_comments.csv")
        self.assertTrue(os.path.exists(posts_file_path))
        self.assertTrue(os.path.exists(comments_file_path))

        if os.path.exists(posts_file_path):
            os.remove(posts_file_path)
        if os.path.exists(comments_file_path):
            os.remove(comments_file_path)

class TestRedditScraper(unittest.TestCase):
    @patch("backend.scraper.reddit_scraper.reddit")
    def test_fetch_brand_data(self, mock_reddit):
        logger.info("Running test_fetch_brand_data")  # Use logging
        mock_submission = MagicMock()
        mock_submission.id = "post1"
        mock_submission.title = "Test Post"
        mock_submission.selftext = "This is a test post."
        mock_submission.score = 100
        mock_submission.url = "http://example.com"
        mock_submission.num_comments = 2
        mock_submission.comments.list.return_value = [
            MagicMock(id="comment1", body="Great post!", score=10),
            MagicMock(id="comment2", body="[deleted]", score=5),
        ]
        mock_reddit.subreddit.return_value.search.return_value = [mock_submission]

        data = fetch_brand_data("TestBrand", limit=1)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["title"], "Test Post")
        self.assertEqual(len(data[0]["comments"]), 2)

if __name__ == "__main__":
    unittest.main()
