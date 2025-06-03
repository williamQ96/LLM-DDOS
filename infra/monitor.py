# infra/monitor.py

import requests
import time

TARGET = "http://localhost:8080"
HISTORY_LEN = 20
_window = []

def record_status():
    try:
        start = time.time()
        r = requests.get(TARGET, timeout=2)
        latency = round((time.time() - start) * 1000, 2)
        _window.append((r.status_code, latency))
    except Exception:
        _window.append(("ERROR", -1))

    # keep recent N records
    if len(_window) > HISTORY_LEN:
        _window.pop(0)

def summarize_observation():
    record_status()
    if not _window:
        return "No data collected."

    code_counts = {}
    total_latency = 0
    valid_latency_count = 0

    for code, latency in _window:
        code_counts[code] = code_counts.get(code, 0) + 1
        if latency >= 0:
            total_latency += latency
            valid_latency_count += 1

    avg_latency = round(total_latency / valid_latency_count, 2) if valid_latency_count else "N/A"
    summary = f"Status codes: {code_counts}. Avg latency: {avg_latency} ms."

    return summary
