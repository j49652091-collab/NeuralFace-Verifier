import cv2
import numpy as np
from PIL import Image
from skimage.feature import local_binary_pattern

# ----------------------------
# Convert image to array
# ----------------------------
def load_image(uploaded_image):

    image = Image.open(uploaded_image).convert("RGB")
    image = np.array(image)
    return image

# ----------------------------
# Face/Eye/Texture signature
# ----------------------------
def extract_signature(image):

    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    # Resize for consistency
    gray = cv2.resize(gray, (200, 200))

    # LBP (Local Binary Pattern) → texture fingerprint
    lbp = local_binary_pattern(gray, P=8, R=1, method="uniform")

    # Histogram = digital signature
    hist, _ = np.histogram(lbp.ravel(), bins=20, range=(0, 20))

    hist = hist.astype("float")
    hist = hist / (hist.sum() + 1e-7)

    return hist

# ----------------------------
# MAIN FUNCTION
# ----------------------------
def detect_image(uploaded_image):

    image = load_image(uploaded_image)

    signature = extract_signature(image)

    # Fake but controlled classification logic
    # (higher variation = more AI-like pattern)
    variance = np.var(signature)

    if variance > 0.01:
        status = "AI / Digital Modified Image"
    else:
        status = "Real Human Image"

    confidence = round((1 - min(variance * 50, 0.99)) * 100, 2)

    return status, confidence, Image.fromarray(image)
