# Red Hat Pins Demo

This repo is forked from [here](https://github.com/redhat-ai-edge-pins-demo/redhat-pins-ai-demo.git).

The original repo only built images for ARM64 - this repo uses a different base image in order to also build for x86_64.

This repo contains a git submodule (`container/yolov5`) so don't forget to clone with the `--recurse-submodules` option.

## Demo

To run the demo, execute the following

	docker compose up

This will start 3 containers:

01. `mediamtx` - this will serve as the RTSP server

01. `ffmpeg` - this streams the sample video (`container/video.mp4`) to `mediamtx`

01. `pins` - this is the Red Hat pins web application; it is configured to use `mediamtx` as a video source via the `VIDEO` environment variable

Once all 3 containers are up, access the pins with a web browser at <http://localhost:8080>


## Running on OpenShift

A sample manifest is located in [`yaml/red-hat-pins.yaml`](yaml/red-hat-pins.yaml).
