import time

class RecommendationCache:
    def __init__(self, ttl_seconds=10):
        self.ttl = ttl_seconds
        self.cache = {}

    def get(self, user_id):
        entry = self.cache.get(user_id)
        if not entry:
            return None

        data, timestamp = entry
        if time.time() - timestamp > self.ttl:
            del self.cache[user_id]
            return None

        return data

    def set(self, user_id, data):
        self.cache[user_id] = (data, time.time())
