import subprocess
import time
import psutil
import re
import os
import datetime

PC_PORT = 5004
DURATION = 30        # 測試秒數
REPORT = "rtp_h264_report.html"

# ffmpeg 命令
cmd = [
    "ffmpeg",
    "-protocol_whitelist", "file,udp,rtp",
    #"-i", f"rtp://0.0.0.0:{PC_PORT}",
    "-i", f"rtp://192.168.50.38:{PC_PORT}",
    "-t", str(DURATION),
    "-f", "null", "-"
]

print("等待 RTP 串流中...")
proc = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.DEVNULL, text=True, bufsize=1)

fps_list = []
bitrate_list = []
start_time = time.time()
last_time = start_time

try:
    while True:
        line = proc.stderr.readline()
        if not line:
            if proc.poll() is not None:
                break
            continue

        line = line.strip()
        # 匹配 ffmpeg 輸出
        if "frame=" in line and "fps=" in line:
            m = re.search(r"frame=\s*(\d+).*fps=\s*([\d\.]+).*bitrate=\s*([\d\.kM]+)", line)
            if m:
                frame = int(m.group(1))
                fps = float(m.group(2))
                bitrate = m.group(3)
                fps_list.append(fps)
                bitrate_list.append(bitrate)

        # 超過測試時間結束
        if time.time() - start_time > DURATION:
            proc.terminate()
            break
except KeyboardInterrupt:
    proc.terminate()

proc.wait()

# 避免 ZeroDivisionError
avg_fps = sum(fps_list)/len(fps_list) if fps_list else 0

# 處理 bitrate，取最後一個或顯示 N/A
last_bitrate = bitrate_list[-1] if bitrate_list else "N/A"

# CPU 使用率
cpu_usage = psutil.cpu_percent(interval=1)

# 生成 HTML 報表
html = f"""
<html>
<head><meta charset="utf-8"><title>ROCK5B+ H264 RTP Test Report</title></head>
<body>
<h1>ROCK5B+ → Windows RTP H264 測試報表</h1>
<p>測試時間: {datetime.datetime.now()}</p>

<table border="1" cellpadding="8">
<tr><th>項目</th><th>結果</th></tr>
<tr><td>平均 FPS</td><td>{avg_fps:.2f}</td></tr>
<tr><td>最後 bitrate</td><td>{last_bitrate}</td></tr>
<tr><td>測試時間</td><td>{DURATION} 秒</td></tr>
<tr><td>接收端 CPU 使用率</td><td>{cpu_usage} %</td></tr>
</table>

<p>結論：ROCK5B+ H264 即時串流能力驗證完成。</p>
</body>
</html>
"""

with open(REPORT, "w", encoding="utf-8") as f:
    f.write(html)

print(f"\n報表已產生：{REPORT}")
print(f"平均 FPS: {avg_fps:.2f}, 最後 bitrate: {last_bitrate}, CPU 使用率: {cpu_usage}%")
