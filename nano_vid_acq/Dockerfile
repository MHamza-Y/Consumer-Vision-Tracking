ARG BASE_IMAGE=nvcr.io/nvidia/l4t-pytorch:r32.4.3-pth1.6-py3
FROM ${BASE_IMAGE}

ENV DEBIAN_FRONTEND=noninteractive

# ====================
# INSTALL COMMON TOOLS
# ====================
RUN apt-get update && apt-get install -y net-tools vim cmake




# ==============
# INSTALL OPENCV
# ==============
COPY jetson-ota-public.asc /etc/apt/trusted.gpg.d/jetson-ota-public.asc
RUN echo "deb https://repo.download.nvidia.com/jetson/common r32.4 main" > /etc/apt/sources.list.d/nvidia-l4t-apt-source.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
            libopencv-python \
    && rm /etc/apt/sources.list.d/nvidia-l4t-apt-source.list \
    && rm -rf /var/lib/apt/lists/*


# =================
# INSTALL GSTREAMER
# =================
RUN apt-get update && \
    apt-get install -y \
    libwayland-egl1 \
    gstreamer1.0-plugins-bad \
    libgstreamer-plugins-bad1.0-0 \
    gstreamer1.0-plugins-good \
    python3-gst-1.0

RUN apt-get update && apt-get install -y supervisor unzip
RUN apt install -y python3-smbus && pip3 install pyzmq

CMD python3 zmq_camera_publisher.py