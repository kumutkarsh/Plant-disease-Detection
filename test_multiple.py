import os
import numpy as np
import tensorflow as tf
from PIL import Image

# -----------------------------
# LOAD MODEL
# -----------------------------
model = tf.keras.models.load_model("plant_disease_model.h5")

# -----------------------------
# CLASS NAMES (FROM DATASET)
# -----------------------------
class_names = sorted(os.listdir("dataset"))
print("📊 Total classes:", len(class_names))

# -----------------------------
# TEST FOLDER (YOUR CASE)
# -----------------------------
folder = "test.jpg"   # ✅ your folder

# check folder exists
if not os.path.exists(folder):
    print("❌ Folder not found:", folder)
    exit()

print("📂 Testing images in:", folder)

# -----------------------------
# LOOP THROUGH IMAGES
# -----------------------------
for file in os.listdir(folder):

    if file.lower().endswith((".jpg", ".jpeg", ".png")):

        print("\n============================")
        print("🖼️ Processing:", file)

        path = os.path.join(folder, file)

        # -----------------------------
        # LOAD IMAGE (SAFE)
        # -----------------------------
        try:
            img = Image.open(path).convert("RGB")
        except:
            print("❌ Cannot open:", file)
            continue

        # preprocess
        img = img.resize((224, 224))
        img = np.array(img) / 255.0
        img = np.reshape(img, (1, 224, 224, 3))

        # -----------------------------
        # PREDICT
        # -----------------------------
        result = model.predict(img, verbose=0)

        index = np.argmax(result)
        confidence = float(np.max(result) * 100)

        full_name = class_names[index]

        # -----------------------------
        # SPLIT PLANT + DISEASE
        # -----------------------------
        parts = full_name.split("___")
        plant = parts[0]

        if "healthy" in full_name.lower():
            disease = "Healthy"
        else:
            disease = parts[1].replace("_", " ")

        # -----------------------------
        # OUTPUT
        # -----------------------------
        print("🌿 Plant:", plant)
        print("🦠 Disease:", disease)
        print("📊 Confidence:", round(confidence, 2), "%")

print("\n✅ Multiple Testing Completed!")