# evaluator.py
def evaluate(results, limits):
    """
    根據測試結果與門檻判定 PASS / FAIL
    :param results: dict, 必須包含 'tcp_dl', 'udp_loss', 'udp_jitter'
    :param limits: dict, 包含 'tcp_dl_min', 'udp_loss_max', 'udp_jitter_max'
    :return: (verdict: bool, reasons: list of str)
    """
    verdict = True
    reasons = []

    tcp_dl = results.get('tcp_dl', 0.0)
    udp_loss = results.get('udp_loss', 100.0)
    udp_jitter = results.get('udp_jitter', 0.0)

    tcp_dl_min = limits.get('tcp_dl_min', 0.0)
    udp_loss_max = limits.get('udp_loss_max', 100.0)
    udp_jitter_max = limits.get('udp_jitter_max', 100.0)

    if tcp_dl < tcp_dl_min:
        verdict = False
        reasons.append(f'TCP DL below threshold ({tcp_dl} < {tcp_dl_min} Mbps)')
    if udp_loss > udp_loss_max:
        verdict = False
        reasons.append(f'UDP loss too high ({udp_loss}% > {udp_loss_max}%)')
    if udp_jitter > udp_jitter_max:
        verdict = False
        reasons.append(f'UDP jitter too high ({udp_jitter} ms > {udp_jitter_max} ms)')

    return verdict, reasons
