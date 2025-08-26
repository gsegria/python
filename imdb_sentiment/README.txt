# 建立虛擬環境
python -m venv venv

# 啟用虛擬環境（Windows）
venv\Scripts\activate

# 安裝所需套件
pip install scikit-learn tensorflow




# 建立虛擬環境
python -m venv venv

# 啟動虛擬環境 (Windows)
venv\Scripts\activate
# Linux/Mac: source venv/bin/activate


imdb_sentiment/
│── imdb_sentiment.py      # 主程式
│── utils.py               # 工具函式（前處理）
│── test_utils.py          # 單元測試 (pytest)
│── requirements.txt       # 套件需求