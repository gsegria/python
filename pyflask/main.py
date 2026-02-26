# main.py

from lib.config import Config
from lib.web_server import start_server
from lib.report import generate_report

def main():

    # ===== 使用者可修改參數 =====
    Config.VIDEO_FOLDER = "video"
    Config.HOST = "0.0.0.0"   # 同機測試用 127.0.0.1
    Config.PORT = 5000
    Config.DATA_UPDATE_HZ = 5
    # ==========================

    print("啟動 HTTP 串流伺服器...")
    start_server()

    print("產生報告...")
    generate_report()

if __name__ == "__main__":
    main()