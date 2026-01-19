import subprocess

PC_IP = "192.168.50.38"
PC_PORT = 5004

ffmpeg_cmd = [
    "ffmpeg",
    "-f", "lavfi",
    "-i", "testsrc2=size=1280x720:rate=30",
    "-c:v", "libx264",      # 軟體編碼
    "-preset", "ultrafast", # 降低 CPU 延遲
    "-b:v", "4M",
    "-f", "rtp",
    f"rtp://{PC_IP}:{PC_PORT}"
]

proc = subprocess.Popen(ffmpeg_cmd)

try:
    proc.wait()
except KeyboardInterrupt:
    proc.terminate()
