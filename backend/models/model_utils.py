from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import cross_val_score
import numpy as np

def get_vectorizer():
    
    return CountVectorizer()

def train_naive_bayes(X, y):
    
    model = MultinomialNB()
    model.fit(X, y)
    return model

def evaluate_model(model, X, y, cv=5):
    
    scores = cross_val_score(model, X, y, cv=cv, scoring="accuracy")
    return scores