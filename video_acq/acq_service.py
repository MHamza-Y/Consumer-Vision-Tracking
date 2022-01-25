import base64

import cv2
import zmq


context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5556")


cap = cv2.VideoCapture(0)
while True:
    socket.recv()
    ret, img = cap.read()
    encoded, buffer = cv2.imencode('.jpg', img)
    jpg_as_text = base64.b64encode(buffer)
    socket.send(jpg_as_text)
