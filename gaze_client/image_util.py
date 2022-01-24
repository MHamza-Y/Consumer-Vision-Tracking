import base64

import cv2
import numpy as np


def decode_image_from_jpg_base64(img_encoded):
    img = base64.b64decode(img_encoded)
    npimg = np.fromstring(img, dtype=np.uint8)
    decoded_image = cv2.imdecode(npimg, 1)
    return decoded_image