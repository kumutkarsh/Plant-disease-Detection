import tensorflow as tf
import numpy as np
from PIL import Image
import os


# Load model
model = tf.keras.models.load_model("plant_disease_model.h5")


# Class labels
class_names = [
    "Corn___Common_Rust", "Corn___Gray_Leaf_Spot", "Corn___Healthy",
    "Corn___Northern_Leaf_Blight", "Potato___Early_Blight", "Potato___Healthy",
    "Potato___Late_Blight", "Rice___Brown_Spot", "Rice___Healthy",
    "Rice___Leaf_Blast", "Rice___Neck_Blast", "Sugarcane___Bacterial_Blight",
    "Sugarcane___Healthy", "Sugarcane___Red_Rot", "Wheat___Brown_Rust",
    "Wheat___Healthy", "Wheat___Yellow_Rust"
]


# Image path
img_path = "test.jpg/image(1).JPG"
print("Path:", img_path)


# Check file
if not os.path.exists(img_path):
    print("❌ File not found")
    exit()


# Load image
try:
    img = Image.open(img_path).convert("RGB")
except Exception as e:
    print("Error:", e)
    exit()


# Preprocess
img = img.resize((224, 224))
img = np.array(img) / 255.0
img = np.reshape(img, (1, 224, 224, 3))


# Prediction
pred = model.predict(img, verbose=0)

index = np.argmax(pred)
confidence = float(np.max(pred) * 100)

label = class_names[index]
parts = label.split("___")

plant = parts[0]
disease = "Healthy" if "healthy" in label.lower() else parts[1].replace("_", " ")


# Output
print("\nResult")
print("Plant:", plant)
print("Disease:", disease)
print("Confidence:", round(confidence, 2), "%")