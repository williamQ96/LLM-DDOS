# scripts/fake_traffic.py
import requests, time, random
import redis

TARGET = "http://localhost:8080"
rdb = redis.Redis(host='localhost', port=6379, decode_responses=True)

def simulate_traffic():
    while True:
        try:
            url = f"{TARGET}/nonexistent" if random.random() < 0.2 else TARGET
            start = time.time()
            r = requests.get(url)
            latency = round((time.time() - start) * 1000, 2)
            status = r.status_code

            print(f"[FAKE_TRAFFIC] {status} - {latency} ms")

            # Update Redis with status + latency
            rdb.hset("server_status", mapping={"latency": latency, "status": status})
        except Exception as e:
            print(f"[FAKE_TRAFFIC] Error: {e}")
        time.sleep(random.uniform(0.3, 1.0))

if __name__ == "__main__":
    simulate_traffic()
