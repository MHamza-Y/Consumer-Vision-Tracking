FROM python:3.8.12-slim-buster

RUN apt-get update && DEBIAN_FRONTEND=noninteractive TZ=Europe/Berlin apt-get -y install tzdata && apt-get install ffmpeg libsm6 libxext6   -y

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD python acq_service.py