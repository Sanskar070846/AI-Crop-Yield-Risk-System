import tensorflow as tf
import numpy as np
import json
from PIL import Image

MODEL_PATH = "disease_detection/tomato/model/tomato_disease_model.h5"
LABELS_PATH = "disease_detection/tomato/model/labels.json"

model = tf.keras.models.load_model(MODEL_PATH)

with open(LABELS_PATH, "r") as f:
    labels = json.load(f)

TREATMENTS = {
    "Tomato___Bacterial_spot": "Use copper-based bactericides. Remove infected leaves.",
    "Tomato___Early_blight": "Apply Mancozeb or Chlorothalonil fungicide.",
    "Tomato___Late_blight": "Use Metalaxyl or Ridomil. Avoid overhead irrigation.",
    "Tomato___Leaf_Mold": "Improve ventilation and apply sulfur-based fungicide.",
    "Tomato___Septoria_leaf_spot": "Apply chlorothalonil and remove infected debris.",
    "Tomato___Spider_mites Two-spotted_spider_mite": "Use neem oil or insecticidal soap.",
    "Tomato___Target_Spot": "Apply appropriate fungicides and rotate crops.",
    "Tomato___Tomato_mosaic_virus": "Remove infected plants. No chemical cure available.",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": "Control whiteflies using insecticides.",
    "Tomato___healthy": "No treatment required. Crop is healthy."
}

def predict_disease(image_path):
    img = Image.open(image_path).convert("RGB")
    img = img.resize((224, 224))

    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    predictions = model.predict(img_array)

    class_index = int(np.argmax(predictions))
    confidence = float(np.max(predictions)) * 100

    # ✅ THIS LINE WAS MISSING
    disease = labels[str(class_index)]

    # Severity logic
    if confidence > 85:
        severity = "High"
    elif confidence > 60:
        severity = "Moderate"
    else:
        severity = "Low"

    treatment = TREATMENTS.get(disease, "Consult agricultural expert.")

    return disease, severity, treatment