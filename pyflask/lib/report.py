import os
import datetime

def generate_report():

    now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"output/report_{now}.html"

    os.makedirs("output", exist_ok=True)

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"""
        <html>
        <body>
        <h1>Streaming Report</h1>
        <p>時間: {now}</p>
        <p>串流測試完成</p>
        </body>
        </html>
        """)

    print("報告已產生:", filename)