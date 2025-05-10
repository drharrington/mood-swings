import joblib
import os
from sklearn.preprocessing import normalize

MODEL_PATH = "backend/models/sentiment_model.pkl"
VECTORIZER_PATH = "backend/models/vectorizer.pkl"

def predict_sentiment(texts):
    if not os.path.exists(MODEL_PATH) or not os.path.exists(VECTORIZER_PATH):
        raise FileNotFoundError("Model or vectorizer not found. Make sure to train first.")

    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)

    if isinstance(texts, str):
        texts = [texts]

    vectors = vectorizer.transform(texts)
    normalized = normalize(vectors)

    predictions = model.predict(normalized)
    return predictions

if __name__ == "__main__":
    predict_sentiment()
