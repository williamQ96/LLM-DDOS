import redis

try:
    r = redis.Redis()
    r.ping()
    print("✅ Redis连接成功！")
except Exception as e:
    print("❌ Redis连接失败：", e)
