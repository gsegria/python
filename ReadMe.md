

# imgproc

`imgproc` 是一個 Python 影像處理專案框架，模組化設計，方便擴充至特徵萃取、物件偵測或影片處理。

# imgproc

`imgproc` 是一個 Python 影像處理專案框架，採模組化設計，方便擴充至特徵萃取、物件偵測與影片處理。

---

## 功能

### 📷 單張影像處理
- 讀取影像（JPG / PNG / BMP）
- Resize、灰階、去噪
- 特徵點萃取（ORB / SIFT）
- 簡單物件偵測（輪廓偵測）
- 視覺化特徵與偵測結果

### 🎥 影片處理（可擴充）
- 逐幀前處理 + 特徵萃取 + 偵測
- 輸出處理後影片（MP4 / AVI）

---

## Project Structure

```text
imgproc/
│
├── main.py                  # 主程式入口（影像 / 影片處理流程統一入口）
├── config.ini               # 參數設定（路徑、影像處理參數、影片設定）
├── requirements.txt         # Python 套件依賴
├── README.md                # 專案說明
│
├── data/                    # 測試資料
│   ├── input/               # 輸入影像 / 影片
│   │   ├── input.jpg
│   │   └── input_video.mp4
│   └── output/              # 處理後輸出
│       ├── output.jpg
│       ├── diff.jpg
│       ├── output_video.mp4
│       └── diff_video.mp4
│
├── lib/                     # 核心模組（可重用）
│   ├── __init__.py
│   ├── image_io.py          # 單張影像讀取與存檔
│   ├── video_io.py          # 影片讀取、串流寫入、diff 計算
│   ├── image_pipeline.py    # 影像處理 pipeline（process_image_pipeline）
│   ├── preprocessing.py     # 前處理（resize / denoise）
│   ├── feature_extraction.py# 特徵萃取（ORB / SIFT）
│   ├── detection.py         # 物件偵測（輪廓 / contours）
│   └── utils.py             # 工具函數（畫特徵點、diff image 儲存等）
│
└── tests/                   # 單元測試
    ├── test_io.py
    ├── test_preprocessing.py
    └── test_feature_extraction.py


---
## 專案功能整理

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


## Run

# 建立環境
python3 -m venv venv

# 啟用
source venv/bin/activate

# 安裝
pip install -r requirements.txt

# 設定路徑
export PYTHONPATH=.

# 執行
python tests/test_image_io.py
python tests/test_image_processing.py