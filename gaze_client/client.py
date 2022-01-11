import socket

import cv2
from imagezmq import imagezmq

sender = imagezmq.ImageSender(connect_to='tcp://gaze-point-prediction:5555')
rpi_name = socket.gethostname()
while True:
    print('Reading Frame')
    cap = cv2.VideoCapture(0)
    ret, img = cap.read()
    print('Sending Image to Gaze Point Prediction Service')
    gaze_points = sender.send_image_reqrep(rpi_name, img)
    print(gaze_points)
