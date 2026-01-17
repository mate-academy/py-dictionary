from typing import Hashable, Any


class Dictionary:
    def __init__(self,
                 initial_capacity: int = 8,
                 load_factor: float = 2 / 3) -> None:
        self.capacity = initial_capacity
        self.load_factor = load_factor
        self.size = 0
        self.buckets = [[] for _ in range(self.capacity)]

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self._hash(key)
        bucket = self.buckets[index]

        for i, (k, h, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, h, value)
                return

        bucket.append((key, hash(key), value))
        self.size += 1

        if self.size > self.capacity * self.load_factor:
            self._resize()

    def _hash(self, key: Hashable) -> int:
        return hash(key) % self.capacity

    def _resize(self) -> None:
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0

        for bucket in old_buckets:
            for key, _, value in bucket:
                self.__setitem__(key, value)

    def __getitem__(self, key: Hashable) -> Any | None:
        index = self._hash(key)
        bucket = self.buckets[index]

        for i, (k, h, v) in enumerate(bucket):
            if k == key:
                return v
        raise KeyError(f"Key '{key}' not found")

    def __len__(self) -> int:
        return self.size
