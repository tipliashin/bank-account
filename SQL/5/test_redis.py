import redis

r = redis.Redis(host='localhost', port=6379, db=0)
try:
    r.ping()
    print("Redis подключён и отвечает!")
except redis.ConnectionError:
    print("Не удалось подключиться к Redis. Убедись, что сервер запущен.")