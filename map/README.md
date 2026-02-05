
pip install -r requirements.txt
python main.py



## 功能
- 顯示初始軌跡與距離
- 點擊地圖新增測量點，自動計算距離
- 可刪除最後一個測量點
- 切換顯示單位（公尺 / 公分）
- 顯示累積距離
- 互動式地圖，支援瀏覽器操作

## 安裝
1. 建議使用虛擬環境：
```bash
python -m venv venv
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate     # Windows



map_tracker/
│
├─ README.md
├─ requirements.txt
├─ main.py
├─ data/
│   └─ sample_track.json   # 初始軌跡點
└─ output/
    └─ interactive_map.html

# Map Tracker - 地圖軌跡互動量測工具

