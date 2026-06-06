import tensorflow as tf
import numpy as np
import cv2

# =========================
# LOAD MODEL
# =========================
model = tf.keras.models.load_model("plant_disease_model.h5")

# =========================
# CLASS NAMES
# =========================
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

# =========================
# TREATMENTS (MERGED)
# =========================
treatments = {

    # 🌽 CORN
    "Corn___Common_Rust": {
        "medicine": "Apply Mancozeb fungicide",
        "organic": "Neem oil spray",
        "prevention": "Use resistant seeds",
        "fertilizer": "Use nitrogen-balanced fertilizer",
        "risk": "Moderate spread in humid weather"
    },
    "Corn___Gray_Leaf_Spot": {
        "medicine": "Use Azoxystrobin",
        "organic": "Compost tea",
        "prevention": "Crop rotation",
        "fertilizer": "Use potassium-rich fertilizer",
        "risk": "High in wet conditions"
    },
    "Corn___Northern_Leaf_Blight": {
        "medicine": "Use Propiconazole",
        "organic": "Neem spray",
        "prevention": "Avoid high humidity",
        "fertilizer": "Balanced NPK",
        "risk": "Spreads rapidly in cool влаж conditions"
    },

    # 🥔 POTATO
    "Potato___Early_Blight": {
        "medicine": "Use Mancozeb fungicide",
        "organic": "Apply baking soda spray",
        "prevention": "Rotate crops and remove debris",
        "fertilizer": "Add potassium-rich fertilizer",
        "risk": "High risk in warm weather"
    },
    "Potato___Late_Blight": {
        "medicine": "Metalaxyl fungicide",
        "organic": "Garlic spray",
        "prevention": "Avoid wet leaves",
        "fertilizer": "Use phosphorus fertilizer",
        "risk": "Very high risk, spreads fast"
    },
    "Potato___Healthy": {
        "medicine": "No treatment needed",
        "organic": "Maintain proper watering",
        "prevention": "Regular monitoring",
        "fertilizer": "Use compost",
        "risk": "No risk"
    },

    # 🍚 RICE
    "Rice___Leaf_Blast": {
        "medicine": "Tricyclazole fungicide",
        "organic": "Neem oil",
        "prevention": "Balanced nitrogen",
        "fertilizer": "Use silica-based fertilizer",
        "risk": "High in humid weather"
    },

    # 🌾 WHEAT
    "Wheat___Brown_Rust": {
        "medicine": "Tebuconazole",
        "organic": "Neem spray",
        "prevention": "Use resistant varieties",
        "fertilizer": "Balanced nitrogen",
        "risk": "Moderate spread"
    },

    # 🍅 TOMATO (NEW)
    "Tomato___Bacterial_spot": {
        "medicine": "Spray Copper Oxychloride (2g/L water)",
        "organic": "Use neem oil spray every 5–7 days",
        "prevention": "Avoid overhead watering, remove infected leaves",
        "fertilizer": "Use balanced NPK fertilizer",
        "risk": "Spreads fast in humid conditions"
    },
    "Tomato___Healthy": {
        "medicine": "No treatment needed",
        "organic": "Maintain regular watering",
        "prevention": "Keep monitoring plant health",
        "fertilizer": "Apply compost regularly",
        "risk": "No risk"
    }
}

# =========================
# SEVERITY DETECTION
# =========================
def get_severity(image_path):
    img = cv2.imread(image_path)

    if img is None:
        return "Unknown"

    img = cv2.resize(img, (224, 224))
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower = np.array([10, 50, 50])
    upper = np.array([30, 255, 255])

    mask = cv2.inRange(hsv, lower, upper)

    ratio = np.sum(mask > 0) / mask.size

    if ratio < 0.05:
        return "Mild"
    elif ratio < 0.15:
        return "Moderate"
    else:
        return "Severe"

# =========================
# MAIN PREDICTION FUNCTION
# =========================
def predict_disease(image_path):

    img = cv2.imread(image_path)

    if img is None:
        return "Unknown", "Unknown", 0, {}, "Unknown"

    img = cv2.resize(img, (224, 224))
    img = img / 255.0
    img = np.reshape(img, (1, 224, 224, 3))

    result = model.predict(img, verbose=0)

    index = np.argmax(result)
    confidence = float(np.max(result) * 100)

    full_name = class_names[index]

    # SAFE SPLIT
    parts = full_name.split("___")

    plant = parts[0] if len(parts) > 0 else "Unknown"

    if len(parts) > 1:
        disease = parts[1].replace("_", " ")
    else:
        disease = "Unknown"

    # HEALTHY CHECK
    if "healthy" in full_name.lower():
        disease = "Healthy"

    # LOW CONFIDENCE HARD STOP
    if confidence < 50:
        return plant, "⚠️ Uncertain", round(confidence, 2), {
            "medicine": "Upload clear image",
            "organic": "Better lighting",
            "prevention": "Try again",
            "fertilizer": "Unknown",
            "risk": "Unknown"
        }, "Unknown"

    # =========================
    # 🔥 NEW SMART TREATMENT LOGIC
    # =========================

    # 1️⃣ Try full_name match (best)
    treatment = treatments.get(full_name)

    # 2️⃣ If not found → try disease name match (your logic)
    if treatment is None:
        disease_key = disease.replace(" ", "_")
        treatment = treatments.get(disease_key)

    # 3️⃣ Final fallback (your given code)
    if treatment is None:
        treatment = {
            "medicine": "Consult expert",
            "organic": "No data",
            "prevention": "No data",
            "fertilizer": "No data",
            "risk": "Unknown"
        }

    # 🔥 SMART WARNING (your code)
    if confidence < 60:
        treatment["prevention"] = "Low confidence. Try a clearer image."

    # =========================
    # SEVERITY
    # =========================
    severity = get_severity(image_path)

    return plant, disease, round(confidence, 2), treatment, severity

# =========================
# TEST
# =========================
if __name__ == "__main__":
    image_path = "test.jpg"  # change your image path

    plant, disease, confidence, treatment, severity = predict_disease(image_path)

    print("\n🌿 Plant:", plant)
    print("🦠 Disease:", disease)
    print("📊 Confidence:", confidence, "%")
    print("⚠️ Severity:", severity)

    print("\n💊 Treatment:")
    for key, value in treatment.items():
        print(f"{key.capitalize()}: {value}")