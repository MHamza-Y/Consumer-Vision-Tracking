import glob
import os

import zmq
import json
import csv
from datetime import datetime

save_dir = glob.glob('storage/*/')[0]
save_file = save_dir + 'gaze_follow_output.csv'
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5562")


def write_dict_to_csv(data_dict, path, write_header=False):
    now = datetime.now()
    current_date_time = now.strftime('%d/%m/%Y T %H:%M:%S.%f')[:-3]

    data_dict['timestamp'] = current_date_time
    print(data_dict)
    with open(path, 'a') as f:
        w = csv.DictWriter(f, fieldnames=data_dict.keys())
        if write_header:
            w.writeheader()
        w.writerow(data_dict)


first_write = not os.path.isfile(save_file)

while True:
    message = socket.recv()
    print(save_dir)
    socket.send(b'')
    gaze_objs = json.loads(message)

    for obj in gaze_objs:
        write_dict_to_csv(obj, save_file, first_write)
        first_write = False
