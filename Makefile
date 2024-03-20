IMAGE=ghcr.io/kwkoo/rhpins:12.3.1
BASE_IMAGE=nvcr.io/nvidia/cuda:12.3.1-devel-ubi9
BUILDERNAME=multiarch-builder

BASE:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

.PHONY: run image mediamtx ffmpeg image-training

run:
	docker run \
	  --name pins \
	  --rm \
	  -it \
	  -p 8080:8080 \
	  -e VIDEO="rtsp://`ifconfig en0 | grep 'inet ' | awk '{ print $$2 }'`:8554/mystream" \
	  $(IMAGE)

run-standalone:
	docker run \
	  --name pins \
	  --rm \
	  -it \
	  -p 8080:8080 \
	  -e CAMERA=video.mp4 \
	  --entrypoint /bin/bash \
	  $(IMAGE)

image:
	-mkdir -p $(BASE)/docker-cache
	docker buildx use $(BUILDERNAME) || docker buildx create --name $(BUILDERNAME) --use
	docker buildx build \
	  --push \
	  --platform=linux/amd64,linux/arm64 \
	  --cache-to type=local,dest=$(BASE)/docker-cache,mode=max \
	  --cache-from type=local,src=$(BASE)/docker-cache \
	  --rm \
	  --build-arg BASE_IMAGE=$(BASE_IMAGE) \
	  -t $(IMAGE) \
	  $(BASE)/container

mediamtx:
	docker run \
	  --rm \
	  -it \
	  --name mediamtx \
	  -v ./container:/host \
	  -e MTX_PROTOCOLS=tcp \
	  -e MTX_WEBRTCADDITIONALHOSTS=`ifconfig en0 | grep 'inet ' | awk '{ print $$2 }'` \
	  -p 8554:8554 \
	  -p 1935:1935 \
	  -p 8888:8888 \
	  -p 8889:8889 \
	  -p 8890:8890/udp \
	  -p 8189:8189/udp \
	  bluenviron/mediamtx:latest-ffmpeg

ffmpeg:
	docker exec \
	  -it \
	  -w /host \
	  mediamtx \
	  ffmpeg -re -stream_loop -1 -i video.mp4 -c copy -f rtsp rtsp://localhost:8554/mystream
