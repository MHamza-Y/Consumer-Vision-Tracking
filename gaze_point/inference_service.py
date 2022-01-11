import sys
import imagezmq

from gaze_point_detector import GazePointDetector

detector = GazePointDetector()
print('Initializing Image Hub')
image_hub = imagezmq.ImageHub(open_port='tcp://*:5555')
while True:
    print('Waiting for request')
    rpi_name, image = image_hub.recv_image()
    response = []
    print('Getting Gaze Points')
    try:
        gaze_points = detector.get_gaze_points(image)
        response = gaze_points
    except:
        print("Oops!", sys.exc_info()[0], "occurred.")
    image_hub.send_reply(response)
