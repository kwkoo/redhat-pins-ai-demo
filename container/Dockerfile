FROM nvcr.io/nvidia/cuda:12.3.1-devel-ubi9

RUN \
  yum update -y \
  && \
  yum install -y python3-pip git mesa-libGL libjpeg libpng libjpeg-devel libpng-devel python3-devel \
  && \
  yum clean all

RUN \
  git clone https://github.com/ultralytics/ultralytics.git /ultralytics \
  && \
  cd /ultralytics \
  && \
  pip3 install . \
  && \
  rm -rf /root/.cache \
  && \
  chown -R :0 /ultralytics \
  && \
  chmod -R g=u /ultralytics

WORKDIR /app
EXPOSE 8080

RUN \
  pip3 install flask lapx \
  && \
  rm -rf /root/.cache

CMD ["python3", "./app.py"]

ENV \
  LD_LIBRARY_PATH=/usr/local/cuda/lib64:/usr/local/lib/python3.9/site-packages/nvidia/cudnn/lib \
  CUDA_DIR=/usr/local/cuda \
  CUDA_PATH=/usr/local/cuda \
  CUDA_INSTALL_DIR=/usr/local/cuda \
  CUDA_HOME=/usr/local/cuda \
  NVIDIA_VISIBLE_DEVICES=all \
  HOME=/app \
  CAMERA=/dev/video0

COPY video.mp4 /app/
COPY best.pt /app/
COPY app/ /app

RUN \
  chown -R :0 /app \
  && \
  chmod -R g=u /app
