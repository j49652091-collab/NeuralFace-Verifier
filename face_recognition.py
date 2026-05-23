from deepface import DeepFace
import numpy as np
import hashlib

def get_embedding(image_path):

    try:

        result=DeepFace.represent(
            img_path=image_path,
            model_name="Facenet",
            enforce_detection=False
        )

        return np.array(
            result[0]["embedding"]
        )

    except:

        return None


def create_signature(embedding):

    if embedding is None:

        return "No Signature"

    normalized=embedding/np.linalg.norm(
        embedding
    )

    text=",".join(
        [str(round(x,5))
         for x in normalized]
    )

    signature=hashlib.sha256(
        text.encode()
    ).hexdigest()

    return signature


def compare_faces(img1,img2):

    emb1=get_embedding(img1)
    emb2=get_embedding(img2)

    if emb1 is None or emb2 is None:

        return {

            "similarity":0,

            "signature":
            "No Face",

            "status":
            "Face Detection Failed"
        }

    similarity=np.dot(
        emb1,
        emb2
    )/(
    np.linalg.norm(emb1)
    *
    np.linalg.norm(emb2)
    )

    similarity=round(
        similarity*100,
        2
    )

    signature=create_signature(
        emb1
    )

    if similarity>70:

        status="Match Found"

    else:

        status="No Match"

    return {

        "similarity":
        similarity,

        "signature":
        signature,

        "status":
        status
    }
