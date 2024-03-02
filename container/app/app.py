import base64
import logging
import sys
import os
import threading
import json
import time

import cv2 as cv2
from flask import Flask, redirect, Response
from announcer import MessageAnnouncer
from ultralytics import YOLO
import torch

# do not log access to health probes
class LogFilter(logging.Filter):
    def filter(self, record):
        msg = record.getMessage()
        if "/livez" in msg or "/readyz" in msg: return False
        return True
logging.getLogger("werkzeug").addFilter(LogFilter())

class LeakTracker:
    max_leak_ids = 10
    leak_ids = []
    count = 0

    def update(self, boxes):
        if (boxes.id is None) or (boxes.cls is None):
            return

        cls = boxes.cls.numpy().astype(int)
        ids = boxes.id.numpy().astype(int)
        for idx, cl in enumerate(cls):
            if cl != 1: # 1 refers to paint leaks
                continue

            leak_id = ids[idx]
            known_id = False
            for id in self.leak_ids:
                if id == leak_id:
                    known_id = True
                    break

            if known_id:
                continue

            # we found a new paint leak
            self.count += + 1
            print(f"paint leak id = {leak_id}")
            self.leak_ids.append(leak_id)
            if len(self.leak_ids) > self.max_leak_ids:
                self.leak_ids.pop(0)

app = Flask(__name__, static_url_path='')

def stop_detection_task():
    logging.info("notifying background thread")
    continue_running.clear()
    background_thread.join()
    logging.info("background thread exited cleanly")

def detection_task(camera_device):
    retry = 500
    leak_tracker = LeakTracker()

    logging.info("loading model...")
    model = YOLO('best.pt')
    logging.info("done loading model")

    total_paint_leaks = 0

    cam = cv2.VideoCapture(camera_device)
    retry_pause = False

    while continue_running.is_set():
        result, frame = cam.read()
        if not result:
            print("Video source did not return a frame")
            cam.open(camera_device)
            if retry_pause:
                time.sleep(2)
            else:
                retry_pause = True
            continue

        retry_pause = False
        results = model.track(frame, persist=True)
        if len(results) < 1:
            continue

        result = results[0]
        leak_tracker.update(result.boxes)
        output_frame = result.plot()

        # convert image to base64-encoded JPEG
        im_encoded = cv2.imencode('.jpg', output_frame)[1]
        im_b64 = base64.b64encode(im_encoded.tobytes()).decode('ascii')

        message = {
            "image": im_b64,
            "leaks": leak_tracker.count
        }
        announcer.announce(format_sse(data=json.dumps(message), event="image", retry=retry))

    cam.release()


@app.route("/")
def home():
    return redirect("/index.html")


@app.route("/livez")
@app.route("/readyz")
@app.route("/healthz")
def health():
    return "OK"


def format_sse(data: str, event=None, retry=None) -> str:
    msg = f'data: {data}\n\n'
    if event is not None:
        msg = f'event: {event}\n{msg}'
    if retry is not None:
        msg = f'retry: {retry}\n{msg}'
    return msg

@app.route('/listen', methods=['GET'])
def listen():

    def stream():
        messages = announcer.listen()  # returns a queue.Queue
        while True:
            msg = messages.get()  # blocks until a new message arrives
            yield msg

    return Response(stream(), mimetype='text/event-stream')


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    if torch.cuda.is_available():
        logging.info("CUDA is available")
        torch.cuda.set_device(0)
    else:
        logging.info("CUDA is not available")

    camera_device = os.getenv('CAMERA', '/dev/video0')

    announcer = MessageAnnouncer()

    with app.app_context():
        continue_running = threading.Event()
        continue_running.set()
        background_thread = threading.Thread(
            target=detection_task,
            args=(camera_device,))
        background_thread.start()

    app.run(host='0.0.0.0', port=8080)
    stop_detection_task()
