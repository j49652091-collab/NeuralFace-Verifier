from PIL import Image
import numpy as np
import cv2
from skimage.feature import local_binary_pattern

def detect_image(uploaded_image):

    image=Image.open(
        uploaded_image
    ).convert("RGB")

    img=np.array(image)

    gray=cv2.cvtColor(
        img,
        cv2.COLOR_RGB2GRAY
    )

    gray=cv2.resize(
        gray,
        (200,200)
    )

    lbp=local_binary_pattern(
        gray,
        P=8,
        R=1,
        method="uniform"
    )

    hist,_=np.histogram(
        lbp.ravel(),
        bins=20,
        range=(0,20)
    )

    hist=hist.astype("float")

    hist=hist/(
        hist.sum()+1e-7
    )

    score=round(
        (1-np.var(hist)*50)
        *100,
        2
    )

    score=max(0,min(score,100))

    if score>60:

        status="Real Human"

    else:

        status="AI / Modified"

    return status,score,image
