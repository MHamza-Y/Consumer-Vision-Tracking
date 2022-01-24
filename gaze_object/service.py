import zmq
import json

from object_finder import get_gazed_object

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5561")

while True:
    message = socket.recv()
    message_dict = json.loads(message)
    gaze_objects = get_gazed_object(gaze_points=message_dict['gaze_points'], objects=message_dict['object_predictions'])
    gaze_objects = json.dumps(gaze_objects).encode('ascii')
    socket.send(gaze_objects)
