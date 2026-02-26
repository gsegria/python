# lib/rtsp_server.py
import os
import subprocess
from lib.config import Config
from lib.video_stream import get_first_video

def start_rtsp_server():
    """
    使用 FFmpeg 將影片推送為 RTSP 流
    URL: rtsp://<HOST>:8554/live.sdp
    """
    video_path = get_first_video()
    rtsp_url = f"rtsp://{Config.HOST}:8554/live.sdp"

    if not os.path.exists(video_path):
        raise Exception(f"影片不存在: {video_path}")

    # FFmpeg 指令 (H.264 編碼 + RTSP)
    cmd = [
        "ffmpeg",
        "-re",  # 以實時速度讀取影片
        "-stream_loop", "-1",  # 無限循環
        "-i", video_path,
        "-c:v", "libx264",
        "-f", "rtsp",
        "-rtsp_transport", "tcp",
        rtsp_url
    ]

    print(f"啟動 RTSP 串流: {rtsp_url}")
    subprocess.Popen(cmd)
    return rtsp_url