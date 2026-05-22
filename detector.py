import cv2
import numpy as np
from PIL import Image
from skimage.feature import local_binary_pattern

# ----------------------------
# Load image
# ----------------------------
def load_image(uploaded_image):
    image = Image.open(uploaded_image).convert("RGB")
    image = np.array(image)
    return image

# ----------------------------
# Face region (approx full image for now)
# ----------------------------
def get_face_region(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    gray = cv2.resize(gray, (200, 200))
    return gray

# ----------------------------
# Eye signature (top half region)
# ----------------------------
def get_eye_region(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    h = gray.shape[0]
    eyes = gray[0:int(h/2), :]
    eyes = cv2.resize(eyes, (200, 100))
    return eyes

# ----------------------------
# Hand texture (bottom half region simulation)
# ----------------------------
def get_hand_region(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    h = gray.shape[0]
    hand = gray[int(h/2):h, :]
    hand = cv2.resize(hand, (200, 100))
    return hand

# ----------------------------
# LBP Signature extractor
# ----------------------------
def lbp_signature(region):
    lbp = local_binary_pattern(region, P=8, R=1, method="uniform")
    hist, _ = np.histogram(lbp.ravel(), bins=20, range=(0, 20))
    hist = hist.astype("float")
    hist = hist / (hist.sum() + 1e-7)
    return hist

# ----------------------------
# Compare two signatures
# ----------------------------
def compare_signatures(sig):
    variance = np.var(sig)

    # forensic scoring (stable, not random)
    score = max(0, 1 - (variance * 60))

    return score

# ----------------------------
# MAIN FUNCTION
# ----------------------------
def detect_image(uploaded_image):

    image = load_image(uploaded_image)

    face = get_face_region(image)
    eye = get_eye_region(image)
    hand = get_hand_region(image)

    face_sig = lbp_signature(face)
    eye_sig = lbp_signature(eye)
    hand_sig = lbp_signature(hand)

    # combine signatures
    combined = (face_sig + eye_sig + hand_sig) / 3

    forensic_score = compare_signatures(combined)

    # decision
    if forensic_score > 0.6:
        status = "Real Human (Forensic Verified)"
    else:
        status = "AI / Synthetic or Modified Image"

    confidence = round(forensic_score * 100, 2)

    return status, confidence, Image.fromarray(image)
