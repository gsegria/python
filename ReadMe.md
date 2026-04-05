

# imgproc

`imgproc` 是一個 Python 影像處理專案框架，模組化設計，方便擴充至特徵萃取、物件偵測或影片處理。

## 功能

- 單張影像處理
  - 讀取影像（JPG/PNG/BMP）
  - Resize、灰階、去噪
  - 特徵點萃取（ORB/SIFT）
  - 簡單物件偵測（輪廓偵測）
  - 視覺化特徵與偵測結果
- 可延伸到影片（MP4/AVI）
  - 逐幀前處理 + 特徵 + 偵測
  - 輸出處理後影片

## 專案結構



imgproc/
│
├── main.py # 主程式入口
├── config.ini # 參數設定
├── requirements.txt # Python 套件需求
├── README.md # 專案說明
│
├── lib/ # 模組化演算法與工具
│ ├── image_io.py
│ ├── preprocessing.py
│ ├── feature_extraction.py
│ ├── detection.py
│ └── utils.py
│
└── tests/ # 測試
└── test_image_io.py
    





1️⃣ 專案原本功能整理

目前專案功能以 影像處理（Image Processing） 為主：

模組	功能說明	現有內容
main.py	主程式流程控制	讀取 config.ini，讀影像 → 前處理 → 特徵萃取 → 偵測 → 存檔
lib/image_io.py	影像讀寫	load_image() / save_image()
lib/preprocessing.py	影像前處理	resize, denoise (gaussian/median)
lib/feature_extraction.py	特徵點萃取	ORB / SIFT，回傳 keypoints 和 descriptors
lib/detection.py	物件偵測	簡單輪廓偵測 (Canny + findContours)
lib/utils.py	工具函數	draw_keypoints()
tests/test_image_io.py	單元測試	讀取/存檔測試影像



## 安裝需求

```bash
pip install -r requirements.txt