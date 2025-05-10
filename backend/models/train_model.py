import pandas as pd
import joblib
import os
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from backend.text_vectorizing.text_vectorizer import process_and_vectorize
import logging

LABELED_DATASET_PATH = "backend/data/labeled_dataset.csv"
VECTORIZED_DATA_PATH = "backend/data/vectorized_labeled.csv"
MODEL_PATH = "backend/models/sentiment_model.pkl"
ORIGIN_LABELED_DATASET = "origin_labeled_dataset"

logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

logger = logging.getLogger(__name__)

def train_model():
    logger.info("Vectorizing data...")
    process_and_vectorize(ORIGIN_LABELED_DATASET, LABELED_DATASET_PATH, is_training=True)

    if not os.path.exists(VECTORIZED_DATA_PATH):
        logger.error("Vectorized data not found.")
        return

    df = pd.read_csv(VECTORIZED_DATA_PATH)
    if "category" not in df.columns:
        logger.error("Missing 'category' column in vectorized data.")
        return

    X = df.drop(columns=["category"])
    y = df["category"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y)

    logger.info("Training model...")
    model = MultinomialNB()
    model.fit(X_train, y_train)

    logger.info("Evaluating model...")
    predictions = model.predict(X_test)
    logger.info(classification_report(y_test, predictions))

    joblib.dump(model, MODEL_PATH)
    logger.info(f"Model saved to {MODEL_PATH}")

if __name__ == "__main__":
    train_model()
