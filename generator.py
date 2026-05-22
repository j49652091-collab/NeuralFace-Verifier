from PIL import Image,ImageFilter

def make_real(uploaded_image):

    img=Image.open(uploaded_image)

    output=img.filter(ImageFilter.DETAIL)

    return output
