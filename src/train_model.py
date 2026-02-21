import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib

df = pd.read_csv("data/processed/processed_data.csv")

# Risk classification
def classify_risk(y):
    if y < 2.5:
        return 2  # High Risk
    elif y < 3.5:
        return 1  # Medium Risk
    else:
        return 0  # Low Risk

df['risk'] = df['yield'].apply(classify_risk)

X = df.drop(['yield', 'risk'], axis=1)
y = df['risk']

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

joblib.dump(model, "models/crop_risk_model.pkl")
print("✅ Model Trained and Saved")