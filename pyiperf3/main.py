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
UDP_BITRATE = '50M'
DURATION = 10

LIMITS = {
    'tcp_dl_min': 50,
    'udp_loss_max': 1.0,
    'udp_jitter_max': 10.0
}

OUTPUT_DIR = 'output'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ------------------ INTERFACE DETECTION ------------------
iface_type, iface_name = detect_interface()
print(f"[INFO] 偵測到介面: {iface_type} ({iface_name})")

# ------------------ IPERF TEST ------------------
tcp_json = run_iperf(SERVER_IP, port=SERVER_PORT, duration=DURATION)
udp_json = run_iperf(SERVER_IP, port=SERVER_PORT, udp=True, bitrate=UDP_BITRATE, duration=DURATION)

# ------------------ PARSE METRICS ------------------
tcp_speed = parse_tcp(tcp_json)
udp_metrics = parse_udp(udp_json)
results = {
    'tcp_dl': tcp_speed,
    'udp_loss': udp_metrics['loss_percent'],
    'udp_jitter': udp_metrics['jitter_ms']
}
print(f"[INFO] 測試結果: {results}")

# ------------------ EVALUATE ------------------
verdict, reasons = evaluate(results, LIMITS)
print(f"[INFO] Verdict: {'PASS' if verdict else 'FAIL'}")
if reasons:
    for r in reasons:
        print(f" - {r}")

# ------------------ GENERATE REPORT ------------------
now = datetime.now().strftime('%Y%m%d_%H%M%S')
csv_path = os.path.join(OUTPUT_DIR, f'report_{now}.csv')
rows = [{**results, 'pass': verdict}]
generate_csv(csv_path, rows)

# UDP Loss 曲線圖
bitrate_value = int(UDP_BITRATE.strip('M'))
loss_plot_path = os.path.join(OUTPUT_DIR, f'loss_{now}.png')
plot_curve([bitrate_value], [results['udp_loss']], 'Target BW (Mbps)', 'Loss %', loss_plot_path)

# TCP + UDP 條形圖
bar_plot_path = os.path.join(OUTPUT_DIR, f'bar_{now}.png')
plot_bar({'TCP Mbps': tcp_speed, 'UDP Loss %': results['udp_loss'], 'UDP Jitter ms': results['udp_jitter']},
         'Network Metrics', 'Value', bar_plot_path)

# HTML 報表
html_path = os.path.join(OUTPUT_DIR, f'report_{now}.html')
generate_html(html_path, {
    'date': now,
    'interface': f'{iface_type} ({iface_name})',
    'status': 'PASS' if verdict else 'FAIL',
    'loss_plot': os.path.basename(loss_plot_path),
    'bar_plot': os.path.basename(bar_plot_path)
})

print(f"[INFO] 報表產生完成，請至 {OUTPUT_DIR} 查看")
