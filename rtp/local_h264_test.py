import subprocess, time

cmd = [
    "ffmpeg",
    "-f", "lavfi", "-i", "testsrc2=size=1920x1080:rate=60",
    "-c:v", "h264_v4l2m2m",
    "-b:v", "8M",
    "-pix_fmt", "nv12",
    "-y", "local_h264.mp4"
]

t0 = time.time()
subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
t1 = time.time()

print(f"H264 編碼完成，耗時: {t1-t0:.2f} 秒")
