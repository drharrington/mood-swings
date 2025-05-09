from model_utils import preprocess_text, train_naive_bayes, save_model
import joblib

def train_sentiment_model(training_data, labels):
    """
    Train a Naive Bayes sentiment model and save the vectorizer and model.
    """
    # Step 1: Preprocess the training data
    vectorized_data, vectorizer = preprocess_text(training_data)

    # Step 2: Train the Naive Bayes classifier
    model = train_naive_bayes(vectorized_data, labels)

    # Step 3: Save the vectorizer and model as .pkl files
    save_model(vectorizer, "vectorizer.pkl")
    save_model(model, "model.pkl")

# Example usage
if __name__ == "__main__":
    # Example training data and labels
    training_data = [
        "I love this product!",
        "This is the worst experience I've ever had.",
        "Absolutely fantastic service.",
        "I hate this so much.",
    ]
    labels = [1, 0, 1, 0]  # 1 = Positive, 0 = Negative

    train_sentiment_model(training_data, labels)