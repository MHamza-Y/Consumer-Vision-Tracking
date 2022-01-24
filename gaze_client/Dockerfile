FROM python:3.8.12-slim-buster

ENV LC_CTYPE en_US.UTF-8
ENV LANG en_US.UTF-8
RUN apt-get update && DEBIAN_FRONTEND=noninteractive TZ=Europe/Berlin apt-get -y install tzdata && apt-get install ffmpeg libsm6 libxext6   -y

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD python -u client.py


