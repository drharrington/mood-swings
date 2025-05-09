from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import cross_val_score, train_test_split
import numpy as np
import joblib

def get_vectorizer():
    """
    Returns a CountVectorizer instance.
    """
    return CountVectorizer()

def train_naive_bayes(X, y):
    """
    Trains a Naive Bayes model on the given data.
    """
    model = MultinomialNB()
    model.fit(X, y)
    return model

def evaluate_model(model, X, y, cv=5):
    """
    Evaluates the model using cross-validation.
    """
    scores = cross_val_score(model, X, y, cv=cv, scoring="accuracy")
    return scores

# New helper functions

def save_model(model, path):
    """
    Saves the trained model to a file.
    """
    joblib.dump(model, path)
    print(f"Model saved to {path}")

def load_model(path):
    """
    Loads a model from a file.
    """
    model = joblib.load(path)
    print(f"Model loaded from {path}")
    return model

def preprocess_text(data, vectorizer=None):
    """
    Preprocesses text data using a vectorizer.
    If no vectorizer is provided, a new one is created and fitted.
    """
    if vectorizer is None:
        vectorizer = get_vectorizer()
        X = vectorizer.fit_transform(data)
    else:
        X = vectorizer.transform(data)
    return X, vectorizer

def split_data(X, y, test_size=0.2, random_state=42):
    """
    Splits the data into training and testing sets.
    """
    return train_test_split(X, y, test_size=test_size, random_state=random_state)