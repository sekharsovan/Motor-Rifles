from flask import Flask, request, jsonify
from flask_cors import CORS   
import random

app = Flask(__name__)
CORS(app)  

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Credit Scoring API running"})

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    income = float(data.get("monthly_income", 25000))
    volatility = float(data.get("income_volatility", 0.3))
    cancellation = float(data.get("cancellation_rate", 0.1))

    # Simulated ML logic (mirrors trained model behaviour)
    default_probability = min(
        0.9,
        0.15 + volatility * 0.6 + cancellation * 0.5 - income / 200000
    )

    repayment_probability = 1 - default_probability
    credit_score = int(300 + 600 * repayment_probability)

    if default_probability <= 0.2:
        risk = "Low"
    elif default_probability <= 0.5:
        risk = "Medium"
    else:
        risk = "High"

    return jsonify({
        "credit_score": credit_score,
        "default_probability": round(default_probability, 3),
        "repayment_probability": round(repayment_probability, 3),
        "risk_bucket": risk
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
