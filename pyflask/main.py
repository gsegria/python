from lib.config import Config
from lib.web_server import start_server
from lib.report import generate_report
from lib.rtsp_server import start_rtsp_server
import subprocess
import threading
import time

def main():

    # ===== 使用者可修改參數 =====
    Config.VIDEO_FOLDER = "video"
    Config.HOST = "0.0.0.0"
    Config.PORT = 5000
    Config.DATA_UPDATE_HZ = 5
    # ==========================

    print("啟動 HTTP 串流伺服器...")
    threading.Thread(target=start_server, daemon=True).start()

    print("啟動 RTSP 串流...")
    rtsp_url = start_rtsp_server()

    # time.sleep(1)  # 等 1 秒讓 FFmpeg RTSP server 準備好
    # print("啟動 ffplay 播放 RTSP...")
    # subprocess.Popen(
    #     ["start", "", "ffplay", "-fflags", "nobuffer", "-rtsp_transport", "tcp", rtsp_url],
    #     shell=True
    # )

    print("產生報告...")
    generate_report()

    # 保持主程式運行（可選，防止程式結束後 ffplay 被關掉）
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("主程式已終止")

if __name__ == "__main__":
    main()