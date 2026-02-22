from flask import Flask, render_template, request
from src.predict_risk import predict_risk
from src.alert_system import send_alert
from src.weather_api import get_weather
from src.explainability import explain_prediction

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

if __name__ == "__main__":
    app.run(debug=True)