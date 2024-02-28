# Red Hat Pins Demo

This repo is forked from [here](https://github.com/redhat-ai-edge-pins-demo/redhat-pins-ai-demo.git).

The original repo only built images for ARM64 - this repo uses a different base image in order to also build for x86_64.

This repo contains a git submodule (`container/yolov5`) so don't forget to clone with the `--recurse-submodules` option.

## Demo

The following steps show how you would run the Red Hat Pins web app on a local docker instance using an RTSP server as a video source.

01. Start [mediamtx](https://github.com/bluenviron/mediamtx) - this will serve as the RTSP server

		make mediamtx

01. Start streaming the sample video through mediamtx - open a new terminal and enter the following

		make ffmpeg

01. Start the Red Hat Pins web application - open a new terminal and enter the following

		make run

	This points the application to the RTSP server by setting the `VIDEO` environment variable


## Running on OpenShift

A sample manifest is located in [`yaml/red-hat-pins.yaml`](yaml/red-hat-pins.yaml).
