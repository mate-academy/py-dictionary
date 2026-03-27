from typing import Any


class Dictionary:
    def __init__(self, capacity: int = 8) -> None:
        self.capacity = capacity
        self.size = 0
        self.buckets = [[] for _ in range(capacity)]
        self.threshold = int(self.capacity * 2 / 3)

    def __setitem__(self, key: str, value: Any) -> None:
        if self.size >= self.threshold:
            self._resize()

        self._insert_no_resize(key, value)

    def __getitem__(self, key: str) -> Any:
        index = self._get_index(key)
        bucket = self.buckets[index]
        for k, h, v in bucket:
            if k == key:
                return v
        raise KeyError(key)

    def __len__(self) -> int:
        return self.size

    def _get_index(self, key: str) -> int:
        return hash(key) % self.capacity

    def _insert_no_resize(self, key: str, value: Any) -> None:
        index = self._get_index(key)
        bucket = self.buckets[index]
        key_hash = hash(key)

        for i, (k, h, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, key_hash, value)
                return

        bucket.append((key, key_hash, value))
        self.size += 1

    def _resize(self) -> None:
        temp_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [[] for _ in range(self.capacity)]
        self.threshold = int(self.capacity * 2 / 3)
        self.size = 0
        for bucket in temp_buckets:
            for k, h, v in bucket:
                self._insert_no_resize(k, v)
