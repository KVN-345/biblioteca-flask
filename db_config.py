# Sustituto simple de Redis usando un diccionario en memoria
class FakeRedis:
    def __init__(self):
        self.store = {}

    def hset(self, key, mapping):
        self.store[key] = mapping

    def hgetall(self, key):
        return self.store.get(key, {})

    def keys(self, pattern="*"):
        return list(self.store.keys())

    def delete(self, key):
        if key in self.store:
            del self.store[key]

# Instancia global
r = FakeRedis()
