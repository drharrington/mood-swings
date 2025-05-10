import os
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize
import logging


VECTORIZER_PATH = "backend/models/vectorizer.pkl"

logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

logger = logging.getLogger(__name__)


def load_vectorizer():
    """Load a pre-trained vectorizer if available."""
    if os.path.exists(VECTORIZER_PATH):
        logger.info("Loading existing vectorizer from vectorizer.pkl")
        return joblib.load(VECTORIZER_PATH)
    else:
        logger.info("No pre-trained vectorizer found.")
        return None

def save_vectorizer(vectorizer):
    """Save the trained vectorizer."""
    joblib.dump(vectorizer, VECTORIZER_PATH)
    logger.info(f"Vectorizer saved to {VECTORIZER_PATH}")

def vectorize_text(data, vectorizer=None, is_training=True):
    """Vectorize text data using TfidfVectorizer."""
    if vectorizer is None:
        if is_training:
            vectorizer = TfidfVectorizer(max_features=1000, stop_words="english")
            vectorized_data = vectorizer.fit_transform(data)
            save_vectorizer(vectorizer)
        else:
            raise ValueError("Cannot vectorize without a trained vectorizer in inference mode.")
    else:
        vectorized_data = vectorizer.transform(data)

    normalized_data = normalize(vectorized_data)
    return normalized_data, vectorizer.get_feature_names_out(), vectorizer

def check_class_imbalance(labels):
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
