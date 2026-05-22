from deepface import DeepFace
import numpy as np

# ----------------------------
# Extract face embedding
# ----------------------------
def get_embedding(image_path):

    embedding = DeepFace.represent(
        img_path=image_path,
        model_name="Facenet",
        enforce_detection=False
    )

    return np.array(embedding[0]["embedding"])

# ----------------------------
# Compare two faces
# ----------------------------
def compare_faces(img1, img2):

    emb1 = get_embedding(img1)
    emb2 = get_embedding(img2)

    # Euclidean distance
    distance = np.linalg.norm(emb1 - emb2)

    # convert to similarity score
    similarity = max(0, 1 - distance / 10)

    return round(similarity * 100, 2)
