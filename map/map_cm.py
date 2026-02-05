import numpy as np
from pyproj import Transformer

# -------------------------------
# 使用者輸入兩個點 (lat, lon)
# 例如台南安平附近兩點
lat1, lon1 = 22.99561, 120.21463
#lat2, lon2 = 22.989768, 120.236890  #tainan
lat2, lon2 = 22.99561, 120.21463486



# -------------------------------
# WGS84 → UTM（台南 51N）
transformer = Transformer.from_crs(
    "EPSG:4326",   # WGS84
    "EPSG:32651",  # UTM zone 51N
    always_xy=True
)

# 轉換
e1, n1 = transformer.transform(lon1, lat1)
e2, n2 = transformer.transform(lon2, lat2)

# -------------------------------
# 計算 ENU 相對距離（以第一點為原點）
dx = e2 - e1
dy = n2 - n1
distance_m = np.sqrt(dx**2 + dy**2)      # 公尺
distance_cm = distance_m * 100            # 公分

# -------------------------------
# 輸出結果
print(f"第一點 UTM (E, N) = ({e1:.3f}, {n1:.3f}) m")
print(f"第二點 UTM (E, N) = ({e2:.3f}, {n2:.3f}) m")
print(f"兩點距離 = {distance_m:.3f} m / {distance_cm:.1f} cm")
