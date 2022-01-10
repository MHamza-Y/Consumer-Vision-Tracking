FROM nvcr.io/nvidia/pytorch:21.12-py3

RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive TZ=Europe/Berlin apt-get -y install tzdata
RUN apt-get install ffmpeg libsm6 libxext6  -y

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN wget -q https://github.com/davisking/dlib-models/raw/master/shape_predictor_68_face_landmarks_GTX.dat.bz2 && bunzip2 shape_predictor_68_face_landmarks_GTX.dat.bz2
RUN wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1eN0NysvRNsWaoyJea3w1Tdbt7iPMvjmp' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1eN0NysvRNsWaoyJea3w1Tdbt7iPMvjmp" -O pretrained_model.pkl  && rm -rf /tmp/cookies.txt

COPY . .

CMD python inference.py


