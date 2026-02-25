class _Node:
    def __init__(self, key, value, hash_value):
        self.key = key
        self.value = value
        self.hash = hash_value


class Dictionary:
    def __init__(self, initial_capacity: int = 8, load_factor: float = 0.75):
        self._capacity = initial_capacity
        self._load_factor = load_factor
        self._size = 0
        self._buckets = [[] for _ in range(self._capacity)]

    def __len__(self):
        return self._size

    def _get_index(self, hash_value):
        return hash_value % self._capacity

    def __setitem__(self, key, value):
        hash_value = hash(key)
        index = self._get_index(hash_value)
        bucket = self._buckets[index]

        for node in bucket:
            if node.key == key:
                node.value = value
                return

        bucket.append(_Node(key, value, hash_value))
        self._size += 1

        if self._size / self._capacity > self._load_factor:
            self._resize()

    def __getitem__(self, key):
        hash_value = hash(key)
        index = self._get_index(hash_value)
        bucket = self._buckets[index]

        for node in bucket:
            if node.key == key:
                return node.value

        raise KeyError(key)

    def _resize(self):
        old_buckets = self._buckets
        self._capacity *= 2
        self._buckets = [[] for _ in range(self._capacity)]
        self._size = 0

        for bucket in old_buckets:
            for node in bucket:
                self[node.key] = node.value