import cv2
import os
from lib.config import Config



def get_first_video():
    # 計算絕對路徑，不影響原有架構
    current_dir = os.path.dirname(os.path.abspath(__file__))  # lib/
    project_dir = os.path.abspath(os.path.join(current_dir, ".."))  # 專案根目錄
    video_folder = os.path.join(project_dir, Config.VIDEO_FOLDER)

    if not os.path.exists(video_folder):
        raise Exception(f"影片資料夾不存在: {video_folder}")

    files = [f for f in os.listdir(video_folder) if f.lower().endswith(".mp4")]
    if not files:
        raise Exception(f"{video_folder} 內沒有 mp4 影片")

    # 回傳絕對路徑
    return os.path.join(video_folder, files[0])


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