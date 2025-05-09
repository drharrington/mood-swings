from flask import Flask, request, jsonify
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# Initialize Flask app
app = Flask(__name__)

# Load the pretrained model and vectorizer
vectorizer_path = "vectorizer.pkl"
model_path = "model.pkl"

vectorizer = joblib.load(vectorizer_path)  # Load TfidfVectorizer
model = joblib.load(model_path)  # Load trained MultinomialNB model

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

        # Make prediction
        prediction = model.predict(text_vectorized)[0]  # Get the predicted label
        prediction_proba = model.predict_proba(text_vectorized).max()  # Get the confidence score

        # Return the result
        return jsonify({
            "text": text,
            "prediction": int(prediction),  # Convert to int for JSON serialization
            "confidence": float(prediction_proba)  # Convert to float for JSON serialization
        })

    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)