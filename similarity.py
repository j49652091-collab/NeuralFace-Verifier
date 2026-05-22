from PIL import Image
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def compare_images(img1,img2):

    image1=Image.open(img1).resize((100,100))
    image2=Image.open(img2).resize((100,100))

    image1=np.array(image1).flatten().reshape(1,-1)
    image2=np.array(image2).flatten().reshape(1,-1)

    similarity=cosine_similarity(image1,image2)

    return round(similarity[0][0]*100,2)
