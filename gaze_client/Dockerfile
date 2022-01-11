FROM nvcr.io/nvidia/pytorch:21.12-py3

RUN apt-get update && DEBIAN_FRONTEND=noninteractive TZ=Europe/Berlin apt-get -y install tzdata && apt-get install ffmpeg libsm6 libxext6   -y

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD python client.py


