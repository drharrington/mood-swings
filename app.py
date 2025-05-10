from flask import Flask, request, jsonify
import logging
import os
from flask_cors import CORS
from backend.run_pipeline import run_pipeline

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Enable CORS
CORS(app, origins=["http://localhost:3000", "https://mood-swings.onrender.com"])


@app.route("/analyze", methods=["POST"])
def analyze():
    """API endpoint to analyze sentiment for a given brand."""
    try:
        # Get JSON data from the request
        data = request.get_json()
        brand_name = data.get("brand_name")

        if not brand_name:
            return jsonify({"error": "Brand name is required"}), 400

        # Run the pipeline
        results = run_pipeline(brand_name)
        return jsonify(results)

    except Exception as e:
        logger.error(f"Error in /analyze endpoint: {e}")
        return jsonify({"error": str(e)}), 500


# Read environment variables for configuration
port = int(os.environ.get("PORT", 5000))
debug = os.environ.get("DEBUG", "False") == "True"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port, debug=debug)
