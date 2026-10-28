class Dictionary:
    def __init__(self):
        self._capacity = 8
        self._size = 0
        self._table = [[] for _ in range(self._capacity)]

    def __setitem__(self, key, value):
        index = hash(key) % self._capacity
        bucket = self._table[index]

        for item in bucket:
            if item["key"] == key:
                item["value"] = value
                return

        bucket.append({
            "key": key,
            "hash": hash(key),
            "value": value
        })

        self._size += 1

    def __getitem__(self, key):
        index = hash(key) % self._capacity
        bucket = self._table[index]

        for item in bucket:
            if item["key"] == key:
                return item["value"]

        raise KeyError(key)

    def __len__(self):
        return self._size
