import os
import datetime
import json
from lib.data_generator import get_engineering_data
from lib.config import Config

def generate_report(video_source="video/sample.mp4", extra_info=None):
    """
    產生工程報告 HTML
    video_source: 來源影片/串流
    extra_info: dict，可附加其他訊息
    """
    now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs("output", exist_ok=True)
    filename = f"output/report_{now}.html"

    # 收集當前工程數據快照
    data_snapshot = get_engineering_data()
    if extra_info:
        data_snapshot.update(extra_info)

    # 單位對應表
    units = {
        "time": "s",
        "temperature": "°C",
        "voltage": "V",
        "speed": "m/s"
    }

    # 將數據轉成 JSON 用於前端繪圖（保持原數值，不加單位）
    data_json = json.dumps(data_snapshot)

    # 表格內容：帶單位
    table_rows = ''.join(
        f"<tr><td>{k}</td><td>{v} {units.get(k, '')}</td></tr>"
        for k, v in data_snapshot.items()
    )

    html_content = f"""
    <!DOCTYPE html>
    <html lang="zh-TW">
    <head>
    <meta charset="UTF-8">
    <title>Streaming Report - {now}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{ font-family: Arial; margin: 20px; }}
        h1 {{ color: #333; }}
        .section {{ margin-bottom: 20px; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ccc; padding: 5px 10px; text-align: left; }}
        th {{ background-color: #f0f0f0; }}
    </style>
    </head>
    <body>
        <h1>Streaming Report</h1>
        <div class="section">
            <h2>報告時間</h2>
            <p>{now}</p>
        </div>

        <div class="section">
            <h2>影片/串流來源</h2>
            <p>{video_source}</p>
        </div>

        <div class="section">
            <h2>工程數據快照</h2>
            <table>
                <tr><th>參數</th><th>數值</th></tr>
                {table_rows}
            </table>
        </div>

        <div class="section">
            <h2>即時數據圖表</h2>
            <canvas id="chart" width="800" height="300"></canvas>
        </div>

        <script>
            const chartData = {data_json};
            const labels = Object.keys(chartData);
            const values = Object.values(chartData);
            const ctx = document.getElementById('chart').getContext('2d');
            new Chart(ctx, {{
                type: 'bar',
                data: {{
                    labels: labels,
                    datasets: [{{
                        label: '工程數據',
                        data: values,
                        backgroundColor: 'rgba(54, 162, 235, 0.5)',
                        borderColor: 'rgba(54, 162, 235, 1)',
                        borderWidth: 1
                    }}]
                }},
                options: {{
                    responsive: true,
                    scales: {{
                        y: {{ beginAtZero: true }}
                    }}
                }}
            }});
        </script>

    </body>
    </html>
    """

    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)

    print("報告已產生:", filename)
    return filename