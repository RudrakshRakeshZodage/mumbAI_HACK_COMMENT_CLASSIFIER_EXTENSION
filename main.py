from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import os

# Use absolute paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "models", "clf.pkl") #.h5  .tflite
VECTORIZER_PATH = os.path.join(BASE_DIR, "..", "models", "vectorizer.pkl")

# Load model + vectorizer
clf = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return {"message": "AI Comment Classifier API running."}

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    text = data.get("text", "").strip()

    if not text:
        return jsonify({"error": "Empty input"}), 400

    X = vectorizer.transform([text])
    pred = clf.predict(X)[0]
    proba = max(clf.predict_proba(X)[0])

    label = "AI" if pred == 1 else "Human"
    return jsonify({
        "prediction": label,
        "confidence": round(proba * 100, 2)
    })

if __name__ == "__main__":
    app.run(debug=True)
