FROM python:3.8.12-slim-buster

ENV LC_CTYPE en_US.UTF-8
ENV LANG en_US.UTF-8

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD python -u service.py


