import pandas as pd
import re

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold
import numpy as np
import pickle

def generate_labels_from_comments(comments):
    
    positive_keywords = [
        'great', 'cool', 'amazing', 'excellent', 'love', 'fantastic', 'satisfied',
        'buy again', 'recommend', 'well', 'success', 'happy', 'wonderful', 'awesome',
        'perfect', 'enjoy', 'best', 'positive', 'delight', 'superb', 'outstanding','fast'
    ]
    negative_keywords = [
        'terrible', 'poor', 'waste', 'not', 'disappointed', 'horrible', 'bad',
        'problem', 'awful', 'hate', 'worst', 'negative', 'fail', 'broken', 'angry',
        'sad', 'unhappy', 'frustrated', 'disaster', 'useless', 'annoying', 'slow', 
    ]

    labels = []
    for comment in comments:
        comment_lower = comment.lower()  # Convert to lowercase for case-insensitive matching
        
        # Count occurrences of positive and negative keywords
        positive_count = sum(comment_lower.count(word) for word in positive_keywords)
        negative_count = sum(comment_lower.count(word) for word in negative_keywords)
        
        # Assign label based on counts
        if positive_count > negative_count:
            labels.append(1)  # Positive label
        elif negative_count > positive_count:
            labels.append(0)  # Negative label
        else:
            labels.append(-1)  # Neutral or unknown sentiment
    return labels

# Example preprocessed data
texts = [
    "great product, very satisfied",
    "terrible experience, not recommended",
    "amazing quality, will buy again",
    "poor quality, waste of money",
    "excellent service and fast delivery",
    "Would not buy again",
    "Interesting product, 100%",
]

# Generate labels
labels = generate_labels_from_comments(texts)  # 1 = Positive, 0 = Negative

# Filter out neutral labels (-1)
filtered_texts = [text for text, label in zip(texts, labels) if label != -1]
filtered_labels = [label for label in labels if label != -1]

# Step 1: Convert filtered text to numerical features
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(filtered_texts)

# Step 2: Train the Naive Bayes classifier
model = MultinomialNB()
model.fit(X, filtered_labels)

# Step 3: Evaluate the model using cross-validation
skf = StratifiedKFold(n_splits=3)
scores = cross_val_score(model, X, filtered_labels, cv=skf, scoring="accuracy")

# Step 4: Print the results
print("Cross-Validation Accuracy Scores:", scores)
print("Mean Accuracy:", np.mean(scores))

# Save the model and vectorizer
with open("model.pkl", "wb") as model_file:
    pickle.dump(model, model_file)

with open("vectorizer.pkl", "wb") as vectorizer_file:
    pickle.dump(vectorizer, vectorizer_file)

print("Model and vectorizer saved successfully!")