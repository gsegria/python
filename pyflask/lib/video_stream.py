import cv2
import os
from lib.config import Config

def get_first_video():
    files = [f for f in os.listdir(Config.VIDEO_FOLDER) if f.endswith(".mp4")]
    if not files:
        raise Exception("video 資料夾內沒有 mp4")
    return os.path.join(Config.VIDEO_FOLDER, files[0])

def generate_frames():
    video_path = get_first_video()
    cap = cv2.VideoCapture(video_path)

    while True:
        success, frame = cap.read()
        if not success:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')