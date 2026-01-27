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
        intervals = json_data.get('intervals', [])
        if not intervals:
            return 0.0

        total_bps = 0.0
        count = 0
        for interval in intervals:
            sum_info = interval.get('sum')
            if sum_info and 'bits_per_second' in sum_info:
                total_bps += sum_info['bits_per_second']
                count += 1

        if count == 0:
            return 0.0

        avg_mbps = (total_bps / count) / 1e6
        return round(avg_mbps, 2)
    except Exception as e:
        print(f"[ERROR] 解析 TCP JSON 發生錯誤: {e}")
        return 0.0


def parse_udp(json_data):
    """
    從 iperf3 UDP JSON 結果取得每個 interval 的 loss % 與 jitter ms
    並計算總結值
    返回 dict:
    {
        'loss_percent': 總結 loss %,
        'jitter_ms': 總結 jitter ms,
        'intervals': [
            {'start': float, 'end': float, 'loss_percent': float, 'jitter_ms': float},
            ...
        ]
    }
    """
    if not json_data or 'intervals' not in json_data or 'end' not in json_data:
        print("[WARN] UDP JSON 無效或缺少 intervals/end")
        return {'loss_percent': 100.0, 'jitter_ms': 0.0, 'intervals': []}

    try:
        interval_data = []
        for interval in json_data['intervals']:
            sum_info = interval.get('sum', {})
            start = sum_info.get('start', 0.0)
            end = sum_info.get('end', 0.0)
            lost_percent = sum_info.get('lost_percent', 0.0)
            jitter_ms = sum_info.get('jitter_ms', 0.0)
            interval_data.append({
                'start': start,
                'end': end,
                'loss_percent': round(lost_percent, 2),
                'jitter_ms': round(jitter_ms, 2)
            })

        end_sum = json_data['end'].get('sum', {})
        total_lost_percent = round(end_sum.get('lost_percent', 100.0), 2)
        total_jitter_ms = round(end_sum.get('jitter_ms', 0.0), 2)

        return {
            'loss_percent': total_lost_percent,
            'jitter_ms': total_jitter_ms,
            'intervals': interval_data
        }

    except Exception as e:
        print(f"[ERROR] 解析 UDP JSON 發生錯誤: {e}")
        return {'loss_percent': 100.0, 'jitter_ms': 0.0, 'intervals': []}
