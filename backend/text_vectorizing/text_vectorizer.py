"""
This script processes and vectorizes data from comments.csv and posts.csv,
and saves the vectorized data to vectorized_comments.csv and vectorized_posts.csv.
"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def vectorize_text(data, vectorizer=None):
    """Vectorize text data using TfidfVectorizer."""
    if vectorizer is None:
        vectorizer = TfidfVectorizer(max_features=1000, stop_words="english")
        vectorized_data = vectorizer.fit_transform(data)
    else:
        vectorized_data = vectorizer.transform(data)
    normalized_data = normalize(vectorized_data)  # Normalize the data
    return normalized_data, vectorizer.get_feature_names_out(), vectorizer
    

def check_class_imbalance(labels):
    """Check for class imbalance and log a warning."""
    logger.info("Input labels: %s", labels)
    if labels is not None and not labels.empty:
        class_counts = labels.value_counts()
        logger.info("Class distribution: %s", class_counts)
        imbalance_score = class_counts.min() / class_counts.max()
        if imbalance_score <= 0.2:
            logger.warning("Significant class imbalance detected.")
        else:
            logger.info("Class distribution is balanced.")
    else:
        logger.info("No labels provided or labels are empty.")


def process_and_vectorize():
    """Load, clean, vectorize, and save text data from posts.csv and comments.csv."""
    # Load the CSV files
    try:
        posts_df = pd.read_csv("backend/data/posts.csv")
        comments_df = pd.read_csv("backend/data/comments.csv")
    except FileNotFoundError as e:
        logger.error("Error: %s", e)
        return

    # Extract and clean text columns
    post_texts = (
        posts_df["post_body"].fillna(posts_df["post_title"]).fillna("").str.strip()
    )
    comment_texts = comments_df["comment_body"].fillna("").str.strip()

    # Extract sentiment labels (if available)
    post_labels = posts_df.get(
        "sentiment", None
    )  # Replace "sentiment" with the actual label column name
    comment_labels = comments_df.get("sentiment", None)

    # Filter out empty rows
    post_texts = post_texts[post_texts != ""]
    comment_texts = comment_texts[comment_texts != ""]
    if post_labels is not None:
        post_labels = post_labels.loc[post_texts.index]
    if comment_labels is not None:
        comment_labels = comment_labels.loc[comment_texts.index]

    # Check for class imbalance
    if post_labels is not None:
        check_class_imbalance(post_labels)
    if comment_labels is not None:
        check_class_imbalance(comment_labels)

    # Check if there is any valid text data
    if post_texts.empty and comment_texts.empty:
        logger.warning("No valid text data found in posts or comments.")
        return

    # Vectorize post bodies if not empty
    if not post_texts.empty:
        post_vectors, post_features = vectorize_text(post_texts)
        post_vectors_df = pd.DataFrame(post_vectors.toarray(), columns=post_features)
        if post_labels is not None:
            post_vectors_df["label"] = post_labels.values
        post_vectors_df.to_csv("backend/data/vectorized_posts.csv", index=False)
        logger.info("Vectorized posts saved to vectorized_posts.csv")

    # Vectorize comment bodies if not empty
    if not comment_texts.empty:
        comment_vectors, comment_features = vectorize_text(comment_texts)
        comment_vectors_df = pd.DataFrame(
            comment_vectors.toarray(), columns=comment_features
        )
        if comment_labels is not None:
            comment_vectors_df["label"] = comment_labels.values
        comment_vectors_df.to_csv("backend/data/vectorized_comments.csv", index=False)
        logger.info("Vectorized comments saved to vectorized_comments.csv")


if __name__ == "__main__":
    process_and_vectorize()
