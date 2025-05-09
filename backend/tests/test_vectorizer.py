import unittest
from unittest.mock import patch
import pandas as pd
from backend.text_vectorizing.text_vectorizer import (
    process_and_vectorize,
    vectorize_text,
    check_class_imbalance,
    logger,
)


class TestTextVectorizer(unittest.TestCase):
    def setUp(self):
        logger.info("Setting up test data for TestTextVectorizer")
        self.sample_posts = pd.DataFrame(
            {
                "post_body": ["This is a test post.", "Another test post."],
                "post_title": ["Test Title", "Another Title"],
                "sentiment": [1, 0],
            }
        )
        self.sample_comments = pd.DataFrame(
            {
                "comment_body": ["Great post!", "Not so great."],
                "sentiment": [1, 0],
            }
        )

    @patch("pandas.read_csv")
    def test_process_and_vectorize(self, mock_read_csv):
        logger.info("Running test_process_and_vectorize")
        mock_read_csv.side_effect = [self.sample_posts, self.sample_comments]

        # capture the DataFrames passed to to_csv
        captured = []

        def fake_to_csv(self, *args, **kwargs):
            captured.append(self)

        with patch("pandas.DataFrame.to_csv", new=fake_to_csv):
            process_and_vectorize()

        # Expect two DataFrames (posts then comments)
        self.assertEqual(len(captured), 2)

        posts_df, comments_df = captured
        self.assertIn("label", posts_df.columns)
        self.assertGreater(len(posts_df), 0)
        self.assertIn("label", comments_df.columns)
        self.assertGreater(len(comments_df), 0)

    def test_vectorize_text(self):
        logger.info("Running test_vectorize_text")
        sample_data = [
            "This is a test sentence with unique words.",
            "Another test sentence with different unique words.",
            "More unique words to ensure enough features are generated.",
        ]
        vectors, feature_names = vectorize_text(sample_data)
        self.assertEqual(vectors.shape[0], len(sample_data))
        self.assertGreater(len(feature_names), 0)

    def test_check_class_imbalance(self):
        # Imbalanced labels -> WARNING
        imbalanced_labels = pd.Series([1, 1, 1, 1, 1, 0])
        with self.assertLogs(logger, level="WARNING") as log:
            check_class_imbalance(imbalanced_labels)
        self.assertTrue(
            any(
                "Significant class imbalance detected" in message
                for message in log.output
            )
        )

        # Balanced labels -> INFO
        balanced_labels = pd.Series([1, 0, 1, 0, 1, 0])
        with self.assertLogs(logger, level="INFO") as log:
            check_class_imbalance(balanced_labels)
        self.assertTrue(any("Class distribution" in message for message in log.output))

        # Empty labels -> INFO about empty
        empty_labels = pd.Series([], dtype=float)
        with self.assertLogs(logger, level="INFO") as log:
            check_class_imbalance(empty_labels)
        self.assertTrue(
            any(
                "No labels provided or labels are empty" in message
                for message in log.output
            )
        )


if __name__ == "__main__":
    unittest.main()
