FROM nvcr.io/nvidia/cuda:12.1.0-devel-ubi8 AS builder

RUN \
  curl \
      -Lo /tmp/miniconda.sh \
      https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-`uname -p`.sh \
  && \
  bash /tmp/miniconda.sh -b -p /usr/local/miniconda \
  && \
  rm -f /tmp/miniconda.sh \
  && \
  . /usr/local/miniconda/etc/profile.d/conda.sh \
  && \
  conda create --name app python=3.11 -y \
  && \
  chown -R :0 /usr/local/miniconda \
  && \
  chmod 775 /usr/local/miniconda \
  && \
  chmod -R g=u /usr/local/miniconda

RUN \
  . /usr/local/miniconda/etc/profile.d/conda.sh \
  && \
  conda activate app \
  && \
  pip install --no-cache ultralytics flask lapx \
  && \
  chown -R :0 /usr/local/miniconda/envs \
  && \
  chmod -R g=u /usr/local/miniconda/envs


FROM nvcr.io/nvidia/cuda:12.1.0-runtime-ubi8

ENV HOME=/root

RUN \
  yum update -y \
  && \
  yum install -y mesa-libGL \
  && \
  yum clean all \
  && \
  echo '. /usr/local/miniconda/etc/profile.d/conda.sh' >> $HOME/.bashrc \
  && \
  echo 'conda activate app' >> $HOME/.bashrc

COPY --from=builder --chown=:0 /usr/local/miniconda /usr/local/miniconda

WORKDIR /app
EXPOSE 8080
CMD ["bash", "-l", "-c", "python ./app.py"]

COPY ./video.mp4 /app/
COPY ./best.pt /app/
COPY ./app/ /app

RUN \
  chmod 775 /root \
  && \
  chown -R :0 /app /root \
  && \
  chmod -R g=u /app /root
