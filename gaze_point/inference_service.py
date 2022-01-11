import sys
import imagezmq
from gaze_point_detector import GazePointDetector
import json


detector = GazePointDetector()
print('Initializing Image Hub')
image_hub = imagezmq.ImageHub(open_port='tcp://*:5555')
while True:

    # Waiting for request
    rpi_name, image = image_hub.recv_image()
    response = []
    # Getting Gaze Points
    try:
        gaze_points = detector.get_gaze_points(image)
        response = gaze_points
    except:
        print("Oops!", sys.exc_info()[0], "occurred.")
    response = json.dumps(response)
    response = response.encode('ascii')
    image_hub.send_reply(response)
