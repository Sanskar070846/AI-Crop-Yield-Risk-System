from flask import Flask, render_template, request
from src.predict_risk import predict_risk
from src.alert_system import send_alert
from src.weather_api import get_weather
from src.explainability import explain_prediction
from disease_detection.tomato.predict_disease import predict_disease
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        city = request.form["city"]
        crop = int(request.form["crop"])
        soil_moisture = float(request.form["soil_moisture"])

        # 🌦️ Live weather
        temperature, humidity, rainfall = get_weather(city)

        input_data = {
            "crop": crop,
            "temperature": temperature,
            "rainfall": rainfall,
            "humidity": humidity,
            "soil_moisture": soil_moisture
        }

        risk = predict_risk(input_data)
        alert = send_alert(risk)

        # ✅ Explainability MUST be here
        explanations = explain_prediction(input_data)

        return render_template(
            "index.html",
            city=city,
            temperature=temperature,
            humidity=humidity,
            rainfall=rainfall,
            risk=risk,
            alert=alert,
            explanations=explanations
        )

    except ValueError as e:
        return render_template(
            "index.html",
            error=str(e)
        )

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/disease", methods=["GET"])
def disease_page():
    return render_template("disease.html")

@app.route("/detect-disease", methods=["POST"])
def detect_disease():
    file = request.files["image"]
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    disease, severity, treatment = predict_disease(file_path)
    return render_template(
    "disease.html",
    disease=disease,
    severity=severity,
    treatment=treatment
)

if __name__ == "__main__":
    app.run(debug=True)