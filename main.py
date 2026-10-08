from flask import Flask, render_template, request, jsonify
import joblib
import os

app = Flask(__name__)

MODEL_PATH = os.path.join("models", "phishing_detector.joblib")
model = joblib.load(MODEL_PATH)

@app.route("/")
def main():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    email = data.get("email", "").strip()

    if not email:
        return jsonify({
            "error": "Please enter email content."
        }), 400

    prediction = model.predict([email])[0]

    if prediction == 1:
        result = "Phishing Email"
    else:
        result = "Safe Email"

    return jsonify({
        "prediction": result
    })


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )