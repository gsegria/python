import csv
import matplotlib.pyplot as plt
from jinja2 import Template

def generate_csv(path, rows):
    if not rows:
        print("[WARN] CSV rows 為空，無法寫入")
        return
    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"[INFO] CSV 產生完成: {path}")

def plot_curve(udp_results, img_path):
    if not udp_results:
        return
    bitrates = [int(r['bitrate'].strip('M')) for r in udp_results]
    losses = [r['loss_percent'] for r in udp_results]
    jitters = [r['jitter_ms'] for r in udp_results]

    fig, ax1 = plt.subplots(figsize=(7, 4))
    ax1.set_xlabel('Target BW (Mbps)')
    ax1.set_ylabel('UDP Loss %', color='tab:blue')
    ax1.plot(bitrates, losses, marker='o', color='tab:blue', label='Loss %')
    ax1.tick_params(axis='y', labelcolor='tab:blue')
    ax1.grid(True)

    ax2 = ax1.twinx()
    ax2.set_ylabel('UDP Jitter (ms)', color='tab:red')
    ax2.plot(bitrates, jitters, marker='x', linestyle='--', color='tab:red', label='Jitter ms')
    ax2.tick_params(axis='y', labelcolor='tab:red')

    plt.title('UDP Loss & Jitter vs Target BW')
    fig.tight_layout()
    plt.savefig(img_path)
    plt.close()
    print(f"[INFO] UDP Loss/Jitter 圖表已儲存: {img_path}")

def plot_bar(bar_metrics, title, ylabel, img_path):
    if not bar_metrics:
        return
    labels = list(bar_metrics.keys())
    values = list(bar_metrics.values())
    plt.figure(figsize=(8, 4))
    bars = plt.bar(labels, values, color='skyblue')
    plt.ylabel(ylabel)
    plt.title(title)
    for bar, val in zip(bars, values):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height(), f'{val:.2f}', ha='center', va='bottom')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(img_path)
    plt.close()
    print(f"[INFO] 條形圖已儲存: {img_path}")

def generate_html(path, context, udp_results=None):
    html_template = '''
<html>
<head><title>RF / Network Test Report</title></head>
<body>
<h1>RF / Network Test Report</h1>
<p>Date: {{ date }}</p>
<p>Interface: {{ interface }}</p>
<p><b>Status: {{ status }}</b></p>

<h2>測試條件</h2>
<ul>
<li>TCP 預期最低速度: {{ tcp_min }} Mbps</li>
<li>測試時間: {{ duration }} 秒</li>
</ul>

<h2>測試結果</h2>
<ul>
<li>TCP 實測下載速度: {{ tcp_dl }} Mbps</li>
</ul>

{% if udp_results %}
<h3>UDP 多帶寬測試結果</h3>
<table border="1" cellpadding="4" cellspacing="0">
<tr>
<th>目標帶寬</th>
<th>允許丟包 %</th>
<th>實際丟包 %</th>
<th>Jitter (ms)</th>
<th>Pass/Fail</th>
</tr>
{% for r in udp_results %}
<tr>
<td>{{ r.bitrate }}</td>
<td>{{ r.allowed_loss }}</td>
<td>{{ r.loss_percent }}</td>
<td>{{ r.jitter_ms }}</td>
<td>{{ 'PASS' if r.loss_percent <= r.allowed_loss else 'FAIL' }}</td>
</tr>
{% endfor %}
</table>
{% endif %}

<h3>UDP Loss & Jitter 曲線圖</h3>
<img src="{{ loss_plot }}" alt="Loss/Jitter Plot">

{% if bar_plot %}
<h3>各指標統計條形圖</h3>
<img src="{{ bar_plot }}" alt="Bar Plot">
{% endif %}
</body>
</html>
'''
    template = Template(html_template)
    with open(path, 'w') as f:
        f.write(template.render(**context, udp_results=udp_results))
    print(f"[INFO] HTML 報表已生成: {path}")
