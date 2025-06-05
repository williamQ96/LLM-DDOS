# scripts/fake_traffic.py
import requests
import time
import random

TARGET = "http://localhost:8080"

def simulate_traffic():
    while True:
        try:
            # Randomize load
            if random.random() < 0.2:
                url = f"{TARGET}/nonexistent"  # trigger 404s
            else:
                url = TARGET

            start = time.time()
            r = requests.get(url)
            latency = round((time.time() - start) * 1000, 2)

            print(f"[FAKE_TRAFFIC] {r.status_code} - {latency} ms")
        except Exception as e:
            print(f"[FAKE_TRAFFIC] Error: {e}")
        time.sleep(random.uniform(0.3, 1.0))  # variable request rate

if __name__ == "__main__":
    simulate_traffic()
