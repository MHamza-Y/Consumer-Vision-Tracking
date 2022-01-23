import socket

from imagezmq import imagezmq
import time


gaze_point_req_sender = imagezmq.ImageSender(connect_to='tcp://gaze-point-prediction:5555')
object_detect_req_sender = imagezmq.ImageSender(connect_to='tcp://yolo-service:5557')
acq_image_hub = imagezmq.ImageHub(open_port='tcp://video-acq:5556', REQ_REP=False)
rpi_name = socket.gethostname()
while True:
    start_time = time.time()
    # Reading Frame from acq service
    rpi_name, image = acq_image_hub.recv_image()
    # Sending Image to Gaze Point Prediction Service
    gaze_points = gaze_point_req_sender.send_image_reqrep(rpi_name, image)
    object_predictions = object_detect_req_sender.send_image_reqrep(rpi_name, image)

    end_time = time.time()
    # Gaze Points
    print(object_predictions)
    print(f'Fps:{1/(end_time-start_time)}')
