from deepface import DeepFace
import numpy as np
import hashlib

# ----------------------------
# Extract Face Embedding
# ----------------------------
def get_face_embedding(image_path):

    try:

        embedding = DeepFace.represent(
            img_path=image_path,
            model_name="Facenet",
            enforce_detection=False
        )

        return np.array(
            embedding[0]["embedding"]
        )

    except Exception as e:

        print("Embedding Error:", e)

        return None


# ----------------------------
# Generate Digital Signature
# ----------------------------
def create_digital_signature(embedding):

    if embedding is None:
        return "No Face Signature"

    # normalize vector
    normalized = embedding / np.linalg.norm(
        embedding
    )

    # vector → text
    embedding_text = ",".join(
        [str(round(x,5))
         for x in normalized]
    )

    # SHA256 hash
    signature = hashlib.sha256(
        embedding_text.encode()
    ).hexdigest()

    return signature


# ----------------------------
# Compare two faces
# ----------------------------
def compare_faces(img1, img2):

    emb1 = get_face_embedding(img1)
    emb2 = get_face_embedding(img2)

    if emb1 is None or emb2 is None:

        return {
            "similarity":0,
            "signature":"No Face Found",
            "status":"Face Detection Failed"
        }

    # cosine similarity
    similarity = np.dot(
        emb1,
        emb2
    ) / (

        np.linalg.norm(emb1)
        *
        np.linalg.norm(emb2)

    )

    similarity = round(
        similarity*100,
        2
    )

    signature = create_digital_signature(
        emb1
    )

    if similarity >=70:

        status="Match Found"

    else:

        status="No Match"

    return {

        "similarity":similarity,

        "signature":signature,

        "status":status

    }


# ----------------------------
# Generate single face signature
# ----------------------------
def generate_face_signature(image_path):

    embedding = get_face_embedding(
        image_path
    )

    signature = create_digital_signature(
        embedding
    )

    return signature
