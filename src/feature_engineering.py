import pandas as pd

def create_features(path):
    df = pd.read_csv(path)

    # Simple derived features
    df['temp_rain_ratio'] = df['temperature'] / (df['rainfall'] + 1)
    df['stress_index'] = df['temperature'] * (100 - df['humidity'])

    return df