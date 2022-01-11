import socket

import cv2
from imagezmq import imagezmq

sender = imagezmq.ImageSender(connect_to='tcp://*:5556', REQ_REP=False)
rpi_name = socket.gethostname()

cap = cv2.VideoCapture(0)
while True:
    ret, img = cap.read()
    sender.send_image(rpi_name, img)
