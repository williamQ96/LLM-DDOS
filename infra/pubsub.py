import redis

class PubSubClient:
    def __init__(self, channel='ddos_channel'):
        print(f"[PubSubClient] Connecting to Redis on channel '{channel}'")
        self.redis = redis.Redis(host='localhost', port=6379, decode_responses=True)
        self.channel = channel

    def publish(self, message: str):
        print(f"[PubSubClient] Publishing: {message}")
        self.redis.publish(self.channel, message)

    def subscribe(self):
        print(f"[PubSubClient] Subscribing to channel: {self.channel}")
        pubsub = self.redis.pubsub()
        pubsub.subscribe(self.channel)
        print(f"[PubSubClient] Subscribed. Waiting for messages...")
        return pubsub.listen()
