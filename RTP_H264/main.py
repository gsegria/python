# main.py
import local_h264
from report import generate

# 1️⃣ 定義測試影片路徑
video_file = "sample.mp4"  # ← 確認 sample.mp4 在同一資料夾，或使用完整路徑

# 2️⃣ 執行 H.264 測試
results, summary_lines, overall_pass, timeline_data = local_h264.run(video_file)

# 3️⃣ 生成 HTML 報表
report_path = generate(results, summary_lines, overall_pass, timeline_data)
print(f"Report saved at: {report_path}")


