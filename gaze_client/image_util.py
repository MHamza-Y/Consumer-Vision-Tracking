import base64

import cv2
import numpy as np


def decode_image_from_jpg_base64(img_encoded):
    img = base64.b64decode(img_encoded)
    npimg = np.fromstring(img, dtype=np.uint8)
    decoded_image = cv2.imdecode(npimg, 1)
    return decoded_image


def outline_obj_on_image(img, gaze_points):
    for point in gaze_points:
        label = point['name']
        if not label == 'person':
            pt1 = (int(point['xmin']), int(point['ymin']))
            pt2 = (int(point['xmax']), int(point['ymax']))
            cv2.rectangle(img=img, pt1=pt1, pt2=pt2, color=(255, 124, 0), thickness=2)
            cv2.putText(img, label, (pt1[0], pt1[1] - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 1)
    cv2.imshow('Gaze Object', img)
    cv2.waitKey(30) & 0xff
