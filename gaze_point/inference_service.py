import imagezmq

from gaze_point.gaze_point_detector import GazePointDetector

detector = GazePointDetector()
image_hub = imagezmq.ImageHub(open_port='tcp://*:5555')
while True:
    rpi_name, image = image_hub.recv_image()
    gaze_points = detector.get_gaze_points(image)
    image_hub.send_reply(GazePointDetector)
