import shap
import joblib
import pandas as pd

model = joblib.load("models/crop_risk_model.pkl")

def explain(input_data):
    explainer = shap.TreeExplainer(model)
    df = pd.DataFrame([input_data])
    shap_values = explainer.shap_values(df)

    return shap_values