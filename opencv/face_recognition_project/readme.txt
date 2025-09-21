

先執行 encode_faces.py → 生成 encodings 檔案

確認檔名與 main.py 一致

再執行 main.py 即可運行



face_recognition_project/
│
├─ main.py                # 主程式，負責流程控制 (開啟攝影機 → 偵測 → 辨識 → 顯示結果)
│
├─ detector.py            # 人臉偵測模組 (OpenCV Haar / dlib)
├─ recognizer.py          # 人臉辨識模組 (face_recognition，特徵向量比對)
│
├─ utils.py               # 工具函式 (檔案存取、座標轉換、繪製框線)
│
├─ data/
│   ├─ known_faces/       # 已知人臉資料庫 (存放圖片)
│   │   ├─ Alice.jpg
│   │   ├─ Bob.jpg
│   │   └─ Charlie.png
│   └─ encodings.pickle   # 已知人臉的特徵向量 (序列化檔案)
│
├─ models/
│   └─ haarcascade_frontalface_default.xml   # OpenCV 預訓練模型
│
├─ results/
│   ├─ logs.txt           # 辨識紀錄 (log)
│   ├─ output.jpg         # 單張結果輸出
│   └─ video_output.avi   # 辨識影片錄製檔
│
└─ requirements.txt       # 套件清單 (pip install -r requirements.txt)


face_recognition_project/
│
├─ main.py                # 即時人臉辨識主程式
├─ encode_faces.py        # 建立 encodings 資料庫
│
├─ data/
│   ├─ known_faces/       # 已知人臉照片
│   │   ├─ Alice_01.jpg
│   │   ├─ Alice_02.jpg
│   │   ├─ Bob_01.jpg
│   │   └─ Charlie_01.png
│   └─ encodings_20250921.pickle   # 產生的特徵向量
│
├─ results/
│   ├─ output_Alice_20250921_1010.jpg
│   └─ video_cam0_20250921_1015.avi
│
└─ requirements.txt
