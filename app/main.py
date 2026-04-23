class Pair:
    def __init__(self, key, hash_value, value):
        self.key = key
        self.hash = hash_value
        self.value = value


class Dictionary:
    def __init__(self, initial_capacity=8, load_factor=0.75):
        self._capacity = initial_capacity
        self._load_factor = load_factor
        self._size = 0
        self._buckets = [[] for _ in range(self._capacity)]

    def __len__(self):
        return self._size

    def _check_index(self, hash_value):
        return hash_value % self._capacity

    def __setitem__(self, key, value):
        hash_value = hash(key)
        index = self._check_index(hash_value)
        bucket = self._buckets[index]

        for pair in bucket:
            if pair.hash == hash_value and pair.key == key:
                pair.value = value
                return

        bucket.append(Pair(key, hash_value, value))
        self._size += 1

        if self._size / self._capacity > self._load_factor:
            self._resize()

    def __getitem__(self, key):
        hash_value = hash(key)
        index = self._check_index(hash_value)
        bucket = self._buckets[index]

        for pair in bucket:
            if pair.hash == hash_value and pair.key == key:
                return pair.value

        raise KeyError(key)

    def __delitem__(self, key):
        hash_value = hash(key)
        index = self._check_index(hash_value)
        bucket = self._buckets[index]

        for i, pair in enumerate(bucket):
            if pair.hash == hash_value and pair.key == key:
                del bucket[i]
                self._size -= 1
                return

        raise KeyError(key)

    def get(self, key, default=None):
        hash_value = hash(key)
        index = self._check_index(hash_value)
        bucket = self._buckets[index]

        for pair in bucket:
            if pair.hash == hash_value and pair.key == key:
                return pair.value

        return default

    def pop(self, key, default=None):
        hash_value = hash(key)
        index = self._check_index(hash_value)
        bucket = self._buckets[index]

        for i, pair in enumerate(bucket):
            if pair.hash == hash_value and pair.key == key:
                value = pair.value
                del bucket[i]
                self._size -= 1
                return value

        if default is not None:
            return default

        raise KeyError(key)

    def clear(self):
        self._buckets = [[] for _ in range(self._capacity)]
        self._size = 0

    def update(self, other):
        for key, value in other:
            self[key] = value

    def __iter__(self):
        for bucket in self._buckets:
            for pair in bucket:
                yield pair.key, pair.value

    def _resize(self):
        old_buckets = self._buckets
        self._capacity *= 2
        self._buckets = [[] for _ in range(self._capacity)]
        old_size = self._size
        self._size = 0

        for bucket in old_buckets:
            for pair in bucket:
                self[pair.key] = pair.value

        self._size = old_size
