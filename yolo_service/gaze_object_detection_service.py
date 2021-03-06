import json

import torch
from imagezmq import imagezmq

model = torch.hub.load('ultralytics/yolov5', 'yolov5l', pretrained=True)
print('Initializing Image Hub')
image_hub = imagezmq.ImageHub(open_port='tcp://*:5557')

while True:
    # Waiting for request
    rpi_name, image = image_hub.recv_image()

    results = model(image)
    results_json = results.pandas().xyxy[0].to_json(orient="records").encode('ascii')
    image_hub.send_reply(results_json)
