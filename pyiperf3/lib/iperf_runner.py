import subprocess
import json


def run_iperf(server_ip, port=5201, udp=False, bitrate=None, duration=30, reverse=False):
    """
    執行 iperf3 測試並回傳 JSON

    :param server_ip: iperf3 server IP
    :param port: 連線 port (預設 5201)
    :param udp: 是否使用 UDP
    :param bitrate: UDP 目標頻寬，例如 '50M'
    :param duration: 測試秒數
    :param reverse: 是否反向測試 (-R)
    :return: dict, iperf3 JSON 結果
    """
    cmd = ['iperf3', '-c', server_ip, '-p', str(port), '-t', str(duration), '-J']

    if reverse:
        cmd.append('-R')
    if udp:
        if bitrate is None:
            bitrate = '10M'  # 預設 UDP 頻寬
        cmd.extend(['-u', '-b', bitrate])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] iperf3 執行失敗: {e}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return None
    except json.JSONDecodeError as e:
        print(f"[ERROR] 無法解析 iperf3 JSON: {e}")
        print(f"原始輸出: {result.stdout}")
        return None
