from typing import Any, List, Optional, Tuple


class Dictionary:
    def __init__(self, capacity: int = 8) -> None:
        self.capacity = capacity
        self.buckets: List[Optional[List[Tuple[Any, Any]]]] = [None] * capacity
        self.size = 0
        self.load_factor = 0.75

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.size / self.capacity > self.load_factor:
            self._resize()
        bucket_index = hash(key) % self.capacity
        bucket = self.buckets[bucket_index]
        if bucket is None:
            bucket = []
            self.buckets[bucket_index] = bucket
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
        self.size += 1

    def __getitem__(self, key: Any) -> Any:
        bucket_index = hash(key) % self.capacity
        bucket = self.buckets[bucket_index]
        if bucket is None:
            raise KeyError(key)
        for k, v in bucket:
            if k == key:
                return v
        raise KeyError(key)

    def __len__(self) -> int:
        return self.size

    def _resize(self) -> None:
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [None] * self.capacity
        self.size = 0
        for bucket in old_buckets:
            if bucket is not None:
                for k, v in bucket:
                    self[k] = v
