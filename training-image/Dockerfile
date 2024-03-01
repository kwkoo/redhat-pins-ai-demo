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

WORKDIR /ultralytics

ENV LD_LIBRARY_PATH=/usr/local/cuda/lib64:/usr/local/lib/python3.9/site-packages/nvidia/cudnn/lib

ENV CUDA_DIR=/usr/local/cuda
ENV CUDA_PATH=/usr/local/cuda
ENV CUDA_INSTALL_DIR=/usr/local/cuda
ENV CUDA_HOME=/usr/local/cuda

ENV NVIDIA_VISIBLE_DEVICES=all
