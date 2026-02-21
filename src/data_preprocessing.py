import pandas as pd
import os

RAW_PATH = "data/raw/crop_data.csv"
PROCESSED_DIR = "data/processed"
PROCESSED_PATH = "data/processed/processed_data.csv"

def preprocess_data():
    # Ensure processed directory exists
    os.makedirs(PROCESSED_DIR, exist_ok=True)

    # Read raw data
    df = pd.read_csv(RAW_PATH)

    print("✅ Raw data loaded")
    print(df.head())

    # Encode crop names
    df["crop"] = df["crop"].astype("category").cat.codes

    # Handle missing values
    df.fillna(df.mean(numeric_only=True), inplace=True)

    # Save processed data
    df.to_csv(PROCESSED_PATH, index=False)

    print("✅ Processed data saved at:", PROCESSED_PATH)
    print("📊 Rows:", df.shape[0], "Columns:", df.shape[1])

if __name__ == "__main__":
    preprocess_data()