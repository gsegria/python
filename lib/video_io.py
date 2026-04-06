# lib/video_io.py
import cv2
import os
from typing import Optional
from tqdm import tqdm  # 進度條套件

def read_video(video_path: str):
    """讀取影片，回傳 cv2.VideoCapture 物件"""
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"影片不存在: {video_path}")
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise IOError(f"無法打開影片: {video_path}")
    return cap

def write_video(frames, output_path: str, fps: int = 30, frame_size: Optional[tuple] = None):
    """將影格列表寫入影片"""
    if not frames:
        raise ValueError("frames 不能為空")
    if frame_size is None:
        frame_size = (frames[0].shape[1], frames[0].shape[0])
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, frame_size)
    for f in frames:
        out.write(f)
    out.release()

def frame_diff(frame1, frame2):
    """計算兩張影格差異 (灰階 + absdiff)"""
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    diff = cv2.absdiff(gray1, gray2)
    _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
    return thresh

# ⭐⭐ 核心抽象（image/video 共用）
def process_frame(img, config):
    from lib import preprocessing, feature_extraction, utils, detection

    gray = config['IMAGE'].getboolean('gray_scale', fallback=False)
    resize_w = config['IMAGE'].getint('resize_width', fallback=None)
    resize_h = config['IMAGE'].getint('resize_height', fallback=None)

    denoise_flag = config['PREPROCESSING'].getboolean('denoise', fallback=True)
    denoise_method = config['PREPROCESSING'].get('denoise_method', fallback='gaussian')

    feature_method = config['FEATURE'].get('method', fallback='ORB')
    max_features = config['FEATURE'].getint('max_features', fallback=500)

    original = img.copy()

    if gray:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    if resize_w and resize_h:
        img = preprocessing.resize(img, resize_w, resize_h)

    if denoise_flag:
        img = preprocessing.denoise(img, method=denoise_method)

    keypoints, descriptors = feature_extraction.extract_features(
        img, method=feature_method, max_features=max_features
    )

    img_kp = utils.draw_keypoints(img, keypoints)

    img_detected, contours = detection.detect_objects(img)

    final = img_kp.copy()
    for cnt in contours:
        cv2.drawContours(final, [cnt], -1, (0, 0, 255), 2)

    return original, final

# ⭐⭐ 完整影片流程（全部藏這裡）
def process_video(input_path, output_dir, config):
    cap = read_video(input_path)

    os.makedirs(output_dir, exist_ok=True)

    video_name = config['VIDEO'].get('output_video_name', 'output_video.mp4')
    diff_name = config['VIDEO'].get('diff_video_name', 'diff_video.mp4')
    enable_diff = config['VIDEO'].getboolean('enable_diff', True)

    fps = config['VIDEO'].getint('fps', fallback=None)
    if fps is None:
        fps = cap.get(cv2.CAP_PROP_FPS) or 30

    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or 0
    frames_out = []
    frames_diff = []
    prev_frame = None

    # ⭐ 使用 tqdm 顯示進度
    with tqdm(total=frame_count, desc="Processing video frames") as pbar:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            original, processed = process_frame(frame, config)
            frames_out.append(processed)

            if enable_diff and prev_frame is not None:
                diff = frame_diff(prev_frame, frame)
                diff_bgr = cv2.cvtColor(diff, cv2.COLOR_GRAY2BGR)
                frames_diff.append(diff_bgr)

            prev_frame = frame
            pbar.update(1)

    cap.release()

    # ⭐ output
    out_video = os.path.join(output_dir, video_name)
    write_video(frames_out, out_video, fps=fps)

    if enable_diff:
        diff_video = os.path.join(output_dir, diff_name)
        write_video(frames_diff, diff_video, fps=fps)

    print(f"Processed video saved to {out_video}")
    if enable_diff:
        print(f"Diff video saved to {diff_video}")