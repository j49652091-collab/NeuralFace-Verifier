import numpy as np
from deepface import DeepFace
import hashlib

# ----------------------------
# Extract Face Embedding
# ----------------------------
def get_face_embedding(image_path):

    embedding = DeepFace.represent(
        img_path=image_path,
        model_name="Facenet",
        enforce_detection=False
    )

    return np.array(embedding[0]["embedding"])

# ----------------------------
# Convert embedding → Digital Signature
# ----------------------------
def create_digital_signature(embedding):

    # normalize
    norm = embedding / np.linalg.norm(embedding)

    # convert to string
    embedding_str = ",".join([str(round(x, 5)) for x in norm])

    # hash = digital fingerprint
    signature = hashlib.sha256(embedding_str.encode()).hexdigest()

    return signature

# ----------------------------
# Full pipeline
# ----------------------------
def generate_face_signature(image_path):

    embedding = get_face_embedding(image_path)

    signature = create_digital_signature(embedding)

    return {
        "embedding": embedding,
        "signature": signature
    }
