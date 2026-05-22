from PIL import Image
import random

def detect_image(uploaded_image):

    image=Image.open(uploaded_image)

    score=random.uniform(0,100)

    if score>50:
        result="AI Generated"
    else:
        result="Real Human"

    return result,score,image
