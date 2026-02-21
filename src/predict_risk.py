import joblib
import pandas as pd

model = joblib.load("models/crop_risk_model.pkl")

def predict_risk(input_data):
    df = pd.DataFrame([input_data])
    prediction = model.predict(df)[0]

    return ["Low", "Medium", "High"][prediction]