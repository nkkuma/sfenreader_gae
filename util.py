from PIL import Image
from io import BytesIO

def byte_array_to_image(byte_array):
    return Image.open(BytesIO(byte_array))

def image_to_byte_array(image:Image):
    imgByteArr = BytesIO()
    image.save(imgByteArr, format="PNG")
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr