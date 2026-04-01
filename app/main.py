from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.size = 0
        self.buckets = [[] for _ in range(self.capacity)]

    def __setitem__(self, key: Any, value: Any) -> None:
        index = hash(key) % self.capacity
        bucket = self.buckets[index]

        for i , (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return

        bucket.append((key, value))
        self.size += 1

        if self.size / self.capacity > 0.7:
            self.resize()

    def resize(self) -> None:
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0

        for bucket in old_buckets:
            for key, value in bucket:
                self[key] = value

    def __getitem__(self, key: Any) -> Any:
        index = hash(key) % self.capacity
        bucket = self.buckets[index]

        for k, v in bucket:
            if k == key:
                return v
        raise KeyError

    def __len__(self) -> int:
        return self.size
