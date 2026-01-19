from typing import Hashable


class Dictionary:
    def __init__(self) -> None:
        self.size = 8
        self.count = 0
        self.start_resizing = 0.75
        self._initialize_buckets()

    def _initialize_buckets(self) -> None:
        self.buckets = [[] for _ in range(self.size)]

    def _hash(self, key: Hashable) -> int:
        return hash(key) % self.size

    def _rehash(self) -> None:
        old_buckets = self.buckets
        self.size *= 2
        self._initialize_buckets()
        self.count = 0
        for bucket in old_buckets:
            for key, value in bucket:
                self[key] = value

    def __setitem__(self, key: Hashable, value: Hashable) -> None:
        index = self._hash(key)
        bucket = self.buckets[index]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
        self.count += 1
        if self.count / self.size > self.start_resizing:
            self._rehash()

    def __getitem__(self, key: Hashable) -> Hashable:
        index = self._hash(key)
        bucket = self.buckets[index]
        for k, v in bucket:
            if k == key:
                return v
        raise KeyError(f"Key {key} not found.")

    def __delitem__(self, key: Hashable) -> None:
        index = self._hash(key)
        bucket = self.buckets[index]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self.count -= 1
                return
        raise KeyError(f"Key {key} not found.")

    def __len__(self) -> int:
        return self.count

    def _clear(self) -> None:
        self._initialize_buckets()
        self.count = 0
