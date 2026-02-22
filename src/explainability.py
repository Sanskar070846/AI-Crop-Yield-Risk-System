import joblib
import pandas as pd

MODEL_PATH = "models/crop_risk_model.pkl"

model = joblib.load(MODEL_PATH)

FEATURE_NAMES = [
    "crop",
    "temperature",
    "rainfall",
    "humidity",
    "soil_moisture"
]

def explain_prediction(input_data):
    """
    Returns top 3 important features influencing prediction
    """
    df = pd.DataFrame([input_data])

    importances = model.feature_importances_

    feature_importance = list(zip(FEATURE_NAMES, importances))
    feature_importance.sort(key=lambda x: x[1], reverse=True)

    # Top 3 reasons
    top_factors = feature_importance[:3]

    explanations = []
    for feature, score in top_factors:
        explanations.append(
            f"{feature.replace('_', ' ').title()} influenced risk (weight: {round(score, 2)})"
        )

    return explanations