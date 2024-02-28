# Use an official Python runtime as a parent image

FROM nvcr.io/nvidia/cuda:12.3.1-devel-ubi9

RUN \
  yum update -y \
  && \
  yum install -y python3-pip git mesa-libGL libjpeg libpng libjpeg-devel libpng-devel python3-devel \
  && \
  yum clean all

RUN \
  pip3 install torch==2.1.0 'opencv-python-headless>=4.1.1' flask

# Set the working directory to /app

WORKDIR /app

# Copy the current directory contents into the container at /app
ADD video.mp4 /app/
ADD templates /app/templates
ADD static /app/static
ADD yolov5 /app/yolov5

# Install any dependencies you may need (e.g., OpenCV)
#RUN dnf install -y python3-pip python3-devel mesa-libGL git gcc g++ libjpeg libpng libjpeg-devel libpng-devel v4l-utils libv4l conda
#RUN git clone https://github.com/ultralytics/yolov5
#RUN git config --global --add safe.directory /app/yolov5
RUN \
  pip3 install \
    websockets \
    flask-socketio \
    dill \
    torchvision==0.16 \
    paho-mqtt \
  && \
  sed -i 's/opencv-python/opencv-python-headless/g' yolov5/requirements.txt \
  &&  \
  sed -i 's/torch/#torch/g' yolov5/requirements.txt \
  && \
  pip3 install -r yolov5/requirements.txt \
  && \
  rm -fr ~/.cache/pip

ENV MANPATH=/usr/share/man:
ENV CUDA_PATH=/usr/local/cuda
ENV MODULES_RUN_QUARANTINE="LD_LIBRARY_PATH LD_PRELOAD"
ENV LD_LIBRARY_PATH=/usr/local/cuda/lib64:/usr/local/lib/python3.9/site-packages/nvidia/cudnn/lib
ENV PATH=/opt/conda/bin:/opt/conda/condabin:/root/.local/bin:/root/bin:/usr/share/Modules/bin:/opt/conda/bin:/usr/cuda/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ENV MODULEPATH=/usr/share/Modules/modulefiles:/etc/modulefiles:/usr/share/modulefiles

ENV CUDA_DIR=/usr/local/cuda
ENV CUDA_PATH=/usr/local/cuda
ENV CUDA_INSTALL_DIR=/usr/local/cuda
ENV CUDA_HOME=/usr/local/cuda

ENV NVIDIA_VISIBLE_DEVICES=all

# Define the default command to run when the container starts
CMD ["/app/app.py"]
ENTRYPOINT ["python3"]

COPY best.pt /app/
COPY app.py /app/
