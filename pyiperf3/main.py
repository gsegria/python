# main.py
from datetime import datetime
import os
from lib.interface_detect import detect_interface
from lib.iperf_runner import run_iperf
from lib.metrics import parse_tcp, parse_udp
from lib.evaluator import evaluate
from lib.report import generate_csv, plot_curve, plot_bar, generate_html

# ------------------ CONFIG ------------------
SERVER_IP = "192.168.50.114"
SERVER_PORT = 5202
DURATION = 10  # 測試時間（秒）

TCP_CONDITIONS = {
    'tcp_min_mbps': 50,
}

UDP_CONDITIONS = [
    {'bitrate': '1M', 'allowed_loss': 1.0},
    {'bitrate': '5M', 'allowed_loss': 1.0},
    {'bitrate': '10M', 'allowed_loss': 1.0},
    {'bitrate': '20M', 'allowed_loss': 1.0},
    {'bitrate': '30M', 'allowed_loss': 1.0},
    {'bitrate': '50M', 'allowed_loss': 1.0},
    {'bitrate': '100M', 'allowed_loss': 1.0},
    {'bitrate': '200M', 'allowed_loss': 1.0},
#    {'bitrate': '300M', 'allowed_loss': 1.0},
#    {'bitrate': '500M', 'allowed_loss': 1.0},
#    {'bitrate': '800M', 'allowed_loss': 1.0},
#    {'bitrate': '1000M', 'allowed_loss': 1.0},
]

OUTPUT_DIR = 'output'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ------------------ INTERFACE DETECTION ------------------
iface_type, iface_name = detect_interface()
print(f"[INFO] 偵測到介面: {iface_type} ({iface_name})")

# ------------------ TCP TEST ------------------
tcp_json = run_iperf(SERVER_IP, port=SERVER_PORT, duration=DURATION)
tcp_speed = parse_tcp(tcp_json)
print(f"[INFO] TCP 測試結果: {tcp_speed} Mbps")

# ------------------ UDP TEST ------------------
udp_results = []
for cond in UDP_CONDITIONS:
    udp_json = run_iperf(SERVER_IP, port=SERVER_PORT, udp=True, bitrate=cond['bitrate'], duration=DURATION)
    metrics = parse_udp(udp_json)
    metrics.update(cond)
    udp_results.append(metrics)
    print(f"[INFO] UDP {cond['bitrate']} 測試結果: Loss={metrics['loss_percent']}%, Jitter={metrics['jitter_ms']} ms")

# ------------------ EVALUATE ------------------
tcp_verdict = tcp_speed >= TCP_CONDITIONS['tcp_min_mbps']
udp_verdicts = [r['loss_percent'] <= r['allowed_loss'] for r in udp_results]
verdict = tcp_verdict and all(udp_verdicts)

reasons = []
if not tcp_verdict:
    reasons.append(f"TCP below minimum ({tcp_speed} < {TCP_CONDITIONS['tcp_min_mbps']} Mbps)")
for r in udp_results:
    if r['loss_percent'] > r['allowed_loss']:
        reasons.append(f"UDP {r['bitrate']} loss too高 ({r['loss_percent']}% > {r['allowed_loss']}%)")

print(f"[INFO] Verdict: {'PASS' if verdict else 'FAIL'}")
if reasons:
    for r in reasons:
        print(" -", r)

# ------------------ GENERATE REPORT ------------------
now = datetime.now().strftime('%Y%m%d_%H%M%S')

# CSV
csv_rows = []
for r in udp_results:
    row = {
        'tcp_dl_mbps': tcp_speed,
        'tcp_min_mbps': TCP_CONDITIONS['tcp_min_mbps'],
        'udp_bitrate': r['bitrate'],
        'udp_loss': r['loss_percent'],
        'udp_jitter': r['jitter_ms'],
        'allowed_udp_loss': r['allowed_loss'],
        'duration_sec': DURATION,
        'interface': iface_name,
        'pass': verdict
    }
    csv_rows.append(row)

csv_path = os.path.join(OUTPUT_DIR, f'report_{now}.csv')
generate_csv(csv_path, csv_rows)

# UDP Loss & Jitter 曲線圖
loss_plot_path = os.path.join(OUTPUT_DIR, f'udp_loss_jitter_{now}.png')
plot_curve(udp_results, loss_plot_path)

# TCP/UDP 指標條形圖
bar_metrics = {'TCP Mbps': tcp_speed}
for r in udp_results:
    bar_metrics[f'UDP Loss {r["bitrate"]}'] = r['loss_percent']
bar_plot_path = os.path.join(OUTPUT_DIR, f'bar_metrics_{now}.png')
plot_bar(bar_metrics, 'Network Metrics', 'Value', bar_plot_path)

# HTML Report
html_path = os.path.join(OUTPUT_DIR, f'report_{now}.html')
generate_html(html_path, {
    'date': now,
    'interface': f'{iface_type} ({iface_name})',
    'status': 'PASS' if verdict else 'FAIL',
    'tcp_dl': tcp_speed,
    'tcp_min': TCP_CONDITIONS['tcp_min_mbps'],
    'duration': DURATION,
    'loss_plot': os.path.basename(loss_plot_path),
    'bar_plot': os.path.basename(bar_plot_path)
}, udp_results=udp_results)

print(f"[INFO] 報表產生完成，請至 {OUTPUT_DIR} 查看")
