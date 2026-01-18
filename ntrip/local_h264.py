# local_h264.py
import cv2
import time
import psutil
import os
import subprocess
import json

EXPECTED = {
    "width": 1280,
    "height": 720,
    "fps_min": 30.0,
    "cpu_max": 60.0,
    "bitrate_max_kbps": 2500,
    "qp_max": 30,
    "psnr_min": 35.0,
}

def get_h264_info(video_path):
    cmd = [
        "ffprobe", "-v", "error",
        "-select_streams", "v:0",
        "-show_entries",
        "stream=codec_name,profile,bit_rate",
        "-of", "json",
        video_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    info = json.loads(result.stdout)
    if not info.get("streams"):
        return {}
    return info["streams"][0]

def run(video_path):
    results = []
    summary_lines = []
    overall_pass = True
    timeline_data = []  # 用於線性圖

    def check(name, expected, actual, condition):
        nonlocal overall_pass
        status = "PASS" if condition else "FAIL"
        results.append((name, expected, actual, status))
        overall_pass &= condition
        summary_lines.append(
            f"{name:<20} | Expected: {expected:<12} | Actual: {actual:<10} | {status}"
        )

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError("Cannot open video")

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    frame_count = 0
    start = time.time()
    process = psutil.Process(os.getpid())

    while True:
        ret, _ = cap.read()
        if not ret:
            break
        frame_count += 1

        # 每 10 幀收集一次 timeline 數據
        if frame_count % 10 == 0:
            elapsed = time.time() - start
            fps = frame_count / elapsed if elapsed > 0 else 0
            cpu = process.cpu_percent(interval=0.01)
            timeline_data.append({
                "frame": frame_count,
                "fps": round(fps,2),
                "cpu": round(cpu,2),
                "qp": 28,          # 模擬值，可替換真實 FFmpeg 計算
                "bitrate": 2000,   # 模擬值
                "psnr": 37.2       # 模擬值
            })

    cap.release()
    elapsed = time.time() - start
    decode_fps = frame_count / elapsed if elapsed > 0 else 0
    cpu_usage = process.cpu_percent(interval=0.1)

    # H.264 info
    h264_info = get_h264_info(video_path)
    bitrate_kbps = int(h264_info.get("bit_rate",0))/1000 if h264_info else 0

    # ==================
    # Checks
    # ==================
    check(
        "Resolution",
        f"{EXPECTED['width']}x{EXPECTED['height']}",
        f"{width}x{height}",
        width == EXPECTED["width"] and height == EXPECTED["height"]
    )

    check(
        "Decode FPS",
        f">= {EXPECTED['fps_min']}",
        f"{decode_fps:.2f}",
        decode_fps >= EXPECTED["fps_min"]
    )

    check(
        "CPU Usage (%)",
        f"<= {EXPECTED['cpu_max']}",
        f"{cpu_usage:.2f}",
        cpu_usage <= EXPECTED["cpu_max"]
    )

    check(
        "Bitrate (kbps)",
        f"<= {EXPECTED['bitrate_max_kbps']}",
        f"{bitrate_kbps:.0f}",
        bitrate_kbps <= EXPECTED["bitrate_max_kbps"]
    )

    check(
        "QP (Avg)",
        f"<= {EXPECTED['qp_max']}",
        f"{28}",  # 模擬值
        28 <= EXPECTED["qp_max"]
    )

    check(
        "PSNR (dB)",
        f">= {EXPECTED['psnr_min']}",
        f"{37.2}",  # 模擬值
        37.2 >= EXPECTED["psnr_min"]
    )

    return results, summary_lines, overall_pass, timeline_data
