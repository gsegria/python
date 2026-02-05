
pip install -r requirements.txt
python main.py



經度長度隨緯度改變，公式大約是：

1
°
經度
≈
111320
×
cos
⁡
(
緯度
)
1°經度≈111320×cos(緯度)

緯度 = 22.99561°

cos
⁡
(
22.99561
°
)
≈
0.923
cos(22.99561°)≈0.923
1
°
經度
≈
111320
×
0.923
≈
102
,
760
公尺
1°經度≈111320×0.923≈102,760公尺
2️⃣ 50 公分換算成經度
Δ
經度
=
0.5
102760
≈
0.00000486
°
Δ經度=
102760
0.5
	​

≈0.00000486°






map_tracker/
│
├─ README.md
├─ requirements.txt
├─ main.py
├─ data/
│   └─ sample_track.json   # 初始軌跡點
└─ output/
    └─ interactive_map.html



