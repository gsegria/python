
Run:
# Linux/macOS
source venv/bin/activate

# Windows (PowerShell)
venv\Scripts\activate



python -m venv venv
source venv/bin/activate    # Linux/macOS
venv\Scripts\activate       # Windows

pip install -r requirements.txt


image_denoise_project/
│
├─ main.py # 程式入口
├─ config.ini # 使用者可調整參數
├─ requirements.txt # Python 套件依賴
├─ README.md
├─ lib/
│ ├─ init.py
│ └─ denoise.py # 核心降噪演算法
└─ test_images/
    └─ noisy_image.jpg # 範例影像






---

## 功能特色

- 支援降噪算法：
  - `bilateral` 雙邊濾波（邊緣保護效果佳）
  - `nl_means` 非局部均值去噪（效果更平滑）
- 可調整降噪強度與邊緣保護程度
- 支援彩色或灰階影像
- 顯示原圖與降噪後影像，並可保存結果
- 完整 GitHub 專案結構，方便擴充或批量處理

---

## 安裝方法

1. 克隆專案

```bash
git clone https://github.com/你的帳號/image_denoise_project.git
cd image_denoise_project