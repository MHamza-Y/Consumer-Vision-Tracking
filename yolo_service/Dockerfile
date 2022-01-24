FROM nvcr.io/nvidia/pytorch:21.10-py3
RUN apt-get update && DEBIAN_FRONTEND=noninteractive TZ=Europe/Berlin apt-get -y install tzdata && apt-get install ffmpeg libsm6 libxext6   -y

COPY download_yolo.py .
COPY requirements.txt .
RUN pip install -qr https://raw.githubusercontent.com/ultralytics/yolov5/master/requirements.txt && python download_yolo.py && pip install -r requirements.txt
COPY . .

CMD python -u gaze_object_detection_service.py