from flask import Flask, render_template, request
from src.predict_risk import predict_risk
from src.alert_system import send_alert

print("✅ app.py started")

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    print("✅ Home route accessed")
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    print("✅ Predict route accessed")

    input_data = {
        "crop": int(request.form["crop"]),
        "temperature": float(request.form["temperature"]),
        "rainfall": float(request.form["rainfall"]),
        "humidity": float(request.form["humidity"]),
        "soil_moisture": float(request.form["soil_moisture"])
    }

    risk = predict_risk(input_data)
    alert = send_alert(risk)

    return render_template(
        "index.html",
        risk=risk,
        alert=alert
    )

if __name__ == "__main__":
    print("🚀 Starting Flask server...")
    app.run(host="127.0.0.1", port=5000, debug=True)