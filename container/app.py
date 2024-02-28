import cv2
import base64
import io
import numpy as np
from flask_socketio import emit, SocketIO
from flask import Flask, render_template, current_app
import sys
import time
import torch

import os

external_host = os.environ.get("EXTERNAL_HOST")
external_port = os.environ.get("EXTERNAL_PORT")

app = Flask(__name__, template_folder="/app/templates")
app.secret_key = 'Shadowman42'
sio = SocketIO(app)

dim = (640, 640)
dim_show = (1280, 720)

def get_device():
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")

device = get_device()
print(f"Using device: {device}")

model = torch.hub.load('yolov5', 'custom', path='best.pt', source='local').to(device)

def get_video_frames():
    if cv2.VideoCapture(1).isOpened():
        video_source = 1
        cap = cv2.VideoCapture(video_source)
    elif cv2.VideoCapture(0).isOpened():
        video_source = 0
        cap = cv2.VideoCapture(video_source)
    else:
        video_source = os.environ.get('VIDEO', 'video.mp4')
        print("Video source is set to %s" % video_source)
        cap = cv2.VideoCapture(video_source)

    fps = cap.get(cv2.CAP_PROP_FPS)
    print("Video FPS %d" % fps)
    retry_pause = False

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Video source did not return a frame")
            cap.open(video_source)
            if retry_pause:
                time.sleep(2)
            else:
                retry_pause = True
            continue

        retry_pause = False
        resized = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
        results = model(resized)

        if results.pandas().xyxy[0].empty:
            pass
        else:
            for i in results.pandas().xyxy[0]['name']:
                print(i, file=sys.stdout)

        results_resized = cv2.resize(np.squeeze(results.render()), dim_show, interpolation=cv2.INTER_AREA)
        frame_bytes = cv2.imencode('.jpg', results_resized)[1]
        stringData = base64.b64encode(frame_bytes).decode('utf-8')
        b64_src = 'data:image/jpeg;base64,'
        stringData = b64_src + stringData
        sio.emit('response_back', stringData, namespace="/")

@sio.on('connect')
def connect():
    pass

@sio.on('start-task')
def start_task():
    print('Start background')
    sio.start_background_task(
        generate_frames,
        current_app.get_current_object()
    )

@app.route("/")
@app.route("/home")
def index():
    server_fqdn = os.environ.get('SERVER_FQDN', 'pins-redhat.local')
    return render_template("index.html", server_fqdn=server_fqdn)

if __name__ == "__main__":
    task = sio.start_background_task(get_video_frames)
    sio.run(app, host="0.0.0.0", port=5000, debug=False, allow_unsafe_werkzeug=True)
