# metrics.py
def parse_tcp(json_data):
    """
    從 iperf3 TCP JSON 結果取得下載速度 (Mbps)
    支援多個 interval 計算平均
    """
    if not json_data or 'intervals' not in json_data:
        print("[WARN] TCP JSON 無效或沒有 intervals")
        return 0.0

    try:
        intervals = json_data['intervals']
        if not intervals:
            return 0.0

        total_bps = 0.0
        count = 0
        for interval in intervals:
            total_bps += interval['sum']['bits_per_second']
            count += 1

        avg_mbps = (total_bps / count) / 1e6 if count else 0.0
        return round(avg_mbps, 2)
    except KeyError as e:
        print(f"[ERROR] 解析 TCP JSON 失敗: {e}")
        return 0.0


def parse_udp(json_data):
    """
    從 iperf3 UDP JSON 結果取得 loss % 和 jitter ms
    """
    if not json_data or 'end' not in json_data:
        print("[WARN] UDP JSON 無效或沒有 end 欄位")
        return {'loss_percent': 100.0, 'jitter_ms': 0.0}

    try:
        end = json_data['end']['sum']
        lost_percent = end.get('lost_percent', 0.0)
        jitter_ms = end.get('jitter_ms', 0.0)
        return {
            'loss_percent': round(lost_percent, 2),
            'jitter_ms': round(jitter_ms, 2)
        }
    except KeyError as e:
        print(f"[ERROR] 解析 UDP JSON 失敗: {e}")
        return {'loss_percent': 100.0, 'jitter_ms': 0.0}
