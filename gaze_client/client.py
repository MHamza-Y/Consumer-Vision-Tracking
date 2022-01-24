import socket as sock
from imagezmq import imagezmq
import time
import zmq
import json

from image_util import decode_image_from_jpg_base64

context = zmq.Context()
gaze_object_socket = context.socket(zmq.REQ)

gaze_object_socket.connect("tcp://gaze-object:5561")
gaze_point_req_sender = imagezmq.ImageSender(connect_to='tcp://gaze-point-prediction:5555')
object_detect_req_sender = imagezmq.ImageSender(connect_to='tcp://yolo-service:5557')
#acq_image_hub = imagezmq.ImageHub(open_port='tcp://video-acq:5556', REQ_REP=False)
acq_img_socket = context.socket(zmq.REQ)
acq_img_socket.connect('tcp://video-acq:5556')
rpi_name = sock.gethostname()
while True:
    start_time = time.time()
    # Reading Frame from acq service
    acq_img_socket.send(b'')
    encoded_image = acq_img_socket.recv()
    image = decode_image_from_jpg_base64(encoded_image)
    # Sending Image to Gaze Point Prediction Service
    gaze_points = gaze_point_req_sender.send_image_reqrep(rpi_name, image)
    gaze_points = json.loads(gaze_points)
    object_predictions = object_detect_req_sender.send_image_reqrep(rpi_name, image)
    object_predictions = json.loads(object_predictions)

    gaze_object_payload = {'gaze_points': gaze_points, 'object_predictions': object_predictions}
    gaze_object_payload = json.dumps(gaze_object_payload).encode('ascii')
    gaze_object_socket.send(gaze_object_payload)
    gaze_object_resp = gaze_object_socket.recv()
    print(gaze_object_resp)
    end_time = time.time()
    # Gaze Points
    print(f'Fps:{1 / (end_time - start_time)}')
