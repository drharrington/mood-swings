from flask import Flask, request, jsonify
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Initialize Flask app
app = Flask(__name__)

# Load the pretrained model and vectorizer
with open("model.pkl", "rb") as model_file:
    model = pickle.load(model_file)  # Load trained MultinomialNB model

with open("vectorizer.pkl", "rb") as vectorizer_file:
    vectorizer = pickle.load(vectorizer_file)  # Load CountVectorizer

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Parse JSON payload
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({"error": "Invalid input. Provide 'text' in JSON payload."}), 400

        # Extract text and preprocess
        text = data['text']
        text_vectorized = vectorizer.transform([text])  # Vectorize input text

        # Predict sentiment
        prediction = model.predict(text_vectorized)[0]
        sentiment = "positive" if prediction == 1 else "negative"

        # Return JSON response
        return jsonify({"text": text, "sentiment": sentiment}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)