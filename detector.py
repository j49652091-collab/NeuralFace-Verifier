from PIL import Image
import torch
from transformers import pipeline

classifier=pipeline(
"image-classification",
model="umm-maybe/AI-image-detector"
)

def detect_image(uploaded_image):

    image=Image.open(
    uploaded_image
    )

    result=classifier(image)

    ai_score=0
    real_score=0

    for item in result:

        label=item["label"]
        score=item["score"]

        if "AI" in label:
            ai_score=score

        else:
            real_score=score

    if ai_score>real_score:

        status="AI Generated"

        confidence=round(
        ai_score*100,
        2
        )

    else:

        status="Real Human"

        confidence=round(
        real_score*100,
        2
        )

    return status,confidence,image
