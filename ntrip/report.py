# report.py
from datetime import datetime
import os
import json

def generate(results, summary_lines, final_result, timeline_data,
             output_dir="output", filename_prefix="video_test_report"):

    os.makedirs(output_dir, exist_ok=True)

    # 在檔名加上日期時間
    now_dt = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{filename_prefix}_{now_dt}.html"
    path = os.path.join(output_dir, filename)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Summary 區塊
    summary_html = "<pre>\n=== Video Decode Test Report ===\n"
    summary_html += "\n".join(summary_lines)
    summary_html += "\n</pre>"

    # 表格
    rows = ""
    for name, exp, act, status in results:
        color = "#4CAF50" if status=="PASS" else "#F44336"
        rows += f"""
        <tr>
            <td>{name}</td>
            <td>{exp}</td>
            <td>{act}</td>
            <td style="color:{color}; font-weight:bold;">{status}</td>
        </tr>
        """

    chart_data_json = json.dumps(timeline_data)
    final_color = "#4CAF50" if final_result else "#F44336"
    final_text = "PASS" if final_result else "FAIL"

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Video Decode Test Report</title>
        <style>
            body {{ font-family: Consolas, monospace; margin: 40px; }}
            pre {{ background: #f8f8f8; padding: 15px; border:1px solid #ccc; }}
            table {{ border-collapse: collapse; width:80%; margin-top:20px; }}
            th, td {{ border:1px solid #ccc; padding:8px; text-align:center; }}
            th {{ background-color:#f2f2f2; }}
            .final {{ margin-top:20px; font-size:24px; font-weight:bold; color:{final_color}; }}
            canvas {{ margin-top:30px; }}
            .report-time {{ margin-top:10px; font-size:14px; color:#555; }}
        </style>
    </head>
    <body>
        <h1>Video Decode Test Report</h1>
        <div class="report-time"><b>Generated at:</b> {now}</div>

        {summary_html}

        <table>
            <tr><th>Item</th><th>Expected</th><th>Actual</th><th>Result</th></tr>
            {rows}
        </table>

        <div class="final">FINAL RESULT: {final_text}</div>

        <h2>Performance Timeline</h2>
        <canvas id="perfChart" width="900" height="400"></canvas>

        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <script>
            const data = {chart_data_json};
            const labels = data.map(d => d.frame);
            const fpsData = data.map(d => d.fps);
            const cpuData = data.map(d => d.cpu);
            const qpData = data.map(d => d.qp);
            const bitrateData = data.map(d => d.bitrate);
            const psnrData = data.map(d => d.psnr);

            const ctx = document.getElementById('perfChart').getContext('2d');
            const perfChart = new Chart(ctx, {{
                type: 'line',
                data: {{
                    labels: labels,
                    datasets: [
                        {{ label:'FPS', data:fpsData, borderColor:'rgba(75,192,192,1)', yAxisID:'y' }},
                        {{ label:'CPU (%)', data:cpuData, borderColor:'rgba(255,99,132,1)', yAxisID:'y1' }},
                        {{ label:'QP', data:qpData, borderColor:'rgba(54,162,235,1)', yAxisID:'y2' }},
                        {{ label:'Bitrate', data:bitrateData, borderColor:'rgba(255,206,86,1)', yAxisID:'y3' }},
                        {{ label:'PSNR', data:psnrData, borderColor:'rgba(153,102,255,1)', yAxisID:'y4' }}
                    ]
                }},
                options: {{
                    responsive:true,
                    interaction: {{ mode:'index', intersect:false }},
                    stacked:false,
                    scales:{{
                        y:{{ type:'linear', position:'left', title:{{ display:true, text:'FPS' }} }},
                        y1:{{ type:'linear', position:'right', title:{{ display:true, text:'CPU (%)' }}, grid:{{drawOnChartArea:false}} }},
                        y2:{{ type:'linear', position:'left', offset:true, title:{{ display:true, text:'QP' }} }},
                        y3:{{ type:'linear', position:'right', offset:true, title:{{ display:true, text:'Bitrate (kbps)' }} }},
                        y4:{{ type:'linear', position:'left', offset:true, title:{{ display:true, text:'PSNR' }}, grid:{{drawOnChartArea:false}} }}
                    }}
                }}
            }});
        </script>
    </body>
    </html>
    """

    with open(path,"w",encoding="utf-8") as f:
        f.write(html)
    print(f"HTML report generated: {path}")
    return path
