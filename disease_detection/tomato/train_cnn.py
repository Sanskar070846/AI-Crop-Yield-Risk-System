import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam
import os

# Paths
DATASET_DIR = "disease_detection/tomato/dataset"
MODEL_DIR = "disease_detection/tomato/model"
os.makedirs(MODEL_DIR, exist_ok=True)

IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 5  # increase later if needed

# Data generators
datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2
)

train_data = datagen.flow_from_directory(
    DATASET_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="training"
)

val_data = datagen.flow_from_directory(
    DATASET_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="validation"
)

# Base model
base_model = MobileNetV2(
    input_shape=(224, 224, 3),
    include_top=False,
    weights="imagenet"
)
base_model.trainable = False

# Model
model = Sequential([
    base_model,
    GlobalAveragePooling2D(),
    Dense(128, activation="relu"),
    Dense(train_data.num_classes, activation="softmax")
])

model.compile(
    optimizer=Adam(learning_rate=0.0001),
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

# Train
history = model.fit(
    train_data,
    validation_data=val_data,
    epochs=EPOCHS
)

# Accuracy
train_acc = history.history["accuracy"][-1]
val_acc = history.history["val_accuracy"][-1]

print(f"📊 Final Training Accuracy: {train_acc * 100:.2f}%")
print(f"📊 Final Validation Accuracy: {val_acc * 100:.2f}%")

# Save model
model.save(os.path.join(MODEL_DIR, "tomato_disease_model.h5"))

# Save accuracy
with open(os.path.join(MODEL_DIR, "accuracy.txt"), "w") as f:
    f.write(f"Training Accuracy: {train_acc * 100:.2f}%\n")
    f.write(f"Validation Accuracy: {val_acc * 100:.2f}%\n")

print("✅ Tomato disease model trained and saved")