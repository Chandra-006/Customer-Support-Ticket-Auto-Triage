
# Standard library imports
import pickle  # For loading the trained model and vectorizer
import re      # For text cleaning
import time    # For latency measurement
import os      # For file existence checks
from flask import Flask, request, jsonify  # Flask web framework
from datetime import datetime  # For timestamps


# Initialize Flask app
app = Flask(__name__)


# Load saved model and vectorizer with error handling
try:
    # Check if model and vectorizer files exist
    if not os.path.exists("model.pkl"):
        raise FileNotFoundError("model.pkl not found. Please run train.py first.")
    if not os.path.exists("vectorizer.pkl"):
        raise FileNotFoundError("vectorizer.pkl not found. Please run train.py first.")
    # Load model
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
    # Load vectorizer
    with open("vectorizer.pkl", "rb") as f:
        vectorizer = pickle.load(f)
    print("✅ Model and vectorizer loaded successfully!")
except FileNotFoundError as e:
    print(f"❌ Error: {e}")
    raise
except Exception as e:
    print(f"❌ Error loading model: {e}")
    raise


# Text cleaning function (must match training)
def clean_text(text):
    """
    Clean and normalize input text for prediction.
    - Lowercase
    - Remove non-letter characters
    - Normalize whitespace
    """
    if not isinstance(text, str):
        raise ValueError("Input must be a string")
    text = text.lower()
    text = re.sub(r"[^a-z\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


# Health check route
@app.route("/", methods=["GET"])
def home():
    """
    Health check endpoint to verify API is running.
    """
    return jsonify({
        "status": "running",
        "message": "Customer Support Ticket Auto-Triage API is running!",
        "timestamp": datetime.now().isoformat()
    })


# Prediction route with latency measurement
@app.route("/predict", methods=["POST"])
def predict():
    """
    Predict the category of a support ticket.
    Measures latency and returns prediction, confidence, and timestamp.
    """
    start_time = time.time()  # Start timer for latency
    try:
        # Validate request type
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
        data = request.get_json()
        # Check for empty request
        if data is None:
            return jsonify({"error": "Empty request body"}), 400
        # Check for required 'text' field
        if "text" not in data:
            return jsonify({"error": "Please provide 'text' field"}), 400
        text = data["text"]
        # Validate text input
        if not isinstance(text, str):
            return jsonify({"error": "'text' field must be a string"}), 400
        if len(text.strip()) == 0:
            return jsonify({"error": "'text' field cannot be empty"}), 400
        # Clean and process text
        cleaned_text = clean_text(text)
        if len(cleaned_text) == 0:
            return jsonify({"error": "Text contains no valid characters after cleaning"}), 400
        # Vectorize and predict
        text_vector = vectorizer.transform([cleaned_text])
        prediction = model.predict(text_vector)
        # Get prediction probabilities for confidence score
        prediction_proba = model.predict_proba(text_vector)[0]
        confidence = float(max(prediction_proba))
        # Calculate latency in milliseconds
        latency_ms = (time.time() - start_time) * 1000
        # Return prediction result
        return jsonify({
            "ticket_text": text,
            "predicted_category": prediction[0],
            "confidence": round(confidence, 4),
            "latency_ms": round(latency_ms, 2),
            "timestamp": datetime.now().isoformat()
        })
    except ValueError as e:
        # Handle input validation errors
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        # Handle unexpected errors
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


# Metrics endpoint to get model evaluation metrics
@app.route("/metrics", methods=["GET"])
def metrics():
    """
    Return model evaluation metrics (accuracy, precision, recall, etc.)
    from evaluation_metrics.json if available.
    """
    try:
        # Load evaluation metrics if available
        if os.path.exists("evaluation_metrics.json"):
            import json
            with open("evaluation_metrics.json", "r") as f:
                eval_metrics = json.load(f)
            return jsonify({
                "model_metrics": eval_metrics,
                "api_status": "operational"
            })
        else:
            # Metrics file not found
            return jsonify({
                "message": "Evaluation metrics not available. Run train.py to generate metrics.",
                "api_status": "operational"
            })
    except Exception as e:
        # Handle errors loading metrics
        return jsonify({"error": str(e)}), 500


# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

