class Dictionary:
    def __init__(self, capacity: int = 8, load_factor: float = 2 / 3) -> None:
        self.capacity: int = capacity
        self.load_factor: float = load_factor
        self.size: int = 0
        self.buckets: list[list[tuple[object, object]]] \
            = [[] for _ in range(self.capacity)]

    def _hash(self, key: object) -> int:
        return hash(key) % self.capacity

    def __len__(self) -> int:
        return self.size

    def __setitem__(self, key: object, value: object) -> None:
        index: int = self._hash(key)
        bucket: list[tuple[object, object]] = self.buckets[index]

        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return

        bucket.append((key, value))
        self.size += 1

        if self.size / self.capacity > self.load_factor:
            self._resize()

    def __getitem__(self, key: object) -> object:
        index: int = self._hash(key)
        bucket: list[tuple[object, object]] = self.buckets[index]

        for k, v in bucket:
            if k == key:
                return v
        raise KeyError(f"Key '{key}' not found")

    def __delitem__(self, key: object) -> None:
        index: int = self._hash(key)
        bucket: list[tuple[object, object]] = self.buckets[index]

        for i, (k, _) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self.size -= 1
                return
        raise KeyError(f"Key '{key}' not found")

    def clear(self) -> None:
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0

    def _resize(self) -> None:
        old_buckets: list[list[tuple[object, object]]] = self.buckets
        self.capacity *= 2
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0

        for bucket in old_buckets:
            for key, value in bucket:
                self[key] = value
