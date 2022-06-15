from PIL import Image
from io import BytesIO
import numpy as np

input_shape = (512, 512)


def read_image(file):
    pil_image = Image.open(file)
    return pil_image


def preprocess(image):
    image = np.array(image)

    return image
