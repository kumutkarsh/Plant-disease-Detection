import tensorflow as tf
import numpy as np
import cv2
from PIL import Image   # 🔥 safer than cv2

# -----------------------------
# LOAD MODEL
# -----------------------------
model = tf.keras.models.load_model("plant_disease_model.h5")

# -----------------------------
# CLASS NAMES (MUST MATCH TRAINING)
# -----------------------------
class_names = [
    "Corn___Common_Rust",
    "Corn___Gray_Leaf_Spot",
    "Corn___Healthy",
    "Corn___Northern_Leaf_Blight",
    "Potato___Early_Blight",
    "Potato___Healthy",
    "Potato___Late_Blight",
    "Rice___Brown_Spot",
    "Rice___Healthy",
    "Rice___Leaf_Blast",
    "Rice___Neck_Blast",
    "Sugarcane___Bacterial_Blight",
    "Sugarcane___Healthy",
    "Sugarcane___Red_Rot",
    "Wheat___Brown_Rust",
    "Wheat___Healthy",
    "Wheat___Yellow_Rust"
]

# -----------------------------
# IMAGE PATH (CHANGE HERE 🔥)
# -----------------------------
img_path = "test.jpg/image(1).JPG"   # ✅ your correct path

# -----------------------------
# LOAD IMAGE (SAFE)
# -----------------------------
try:
    img = Image.open(img_path)
except:
    print("❌ Error: Cannot open image")
    exit()

# preprocess
img = img.resize((224, 224))
img = np.array(img) / 255.0
img = np.reshape(img, (1, 224, 224, 3))

# -----------------------------
# PREDICT
# -----------------------------
prediction = model.predict(img, verbose=0)

index = np.argmax(prediction)
confidence = float(np.max(prediction) * 100)

full_name = class_names[index]

# split plant + disease
parts = full_name.split("___")
plant = parts[0]

if "healthy" in full_name.lower():
    disease = "Healthy"
else:
    disease = parts[1].replace("_", " ")

# -----------------------------
# RESULT
# -----------------------------
print("\n✅ RESULT")
print("🌿 Plant:", plant)
print("🦠 Disease:", disease)
print("📊 Confidence:", round(confidence, 2), "%")