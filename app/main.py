from typing import Any


class Dictionary:
    def __init__(self) -> None:
        initial_capacity = 8
        self.buckets = [[] for _ in range(initial_capacity)]
        self.capacity = len(self.buckets)
        self.size = 0

    def __setitem__(self, key: Any, value: Any) -> Any:
        h = hash(key)
        node = (h, key, value)
        idx = h % self.capacity
        bucket = self.buckets[idx]

        for i, (hh, k, v) in enumerate(bucket):
            if k == key and hh == h:
                bucket[i] = (hh, k, value)
                return
        if self.size / self.capacity >= 0.66:
            self._resize()
            idx = h % self.capacity
            bucket = self.buckets[idx]
        bucket.append(node)
        self.size += 1

    def __getitem__(self, key: Any) -> Any:
        h = hash(key)
        idx = h % self.capacity
        buckets = self.buckets[idx]
        for hh, k, v in buckets:
            if k == key:
                return v
        else:
            raise KeyError(f"Key {key} not found!!!")

    def __len__(self) -> int:
        return self.size

    def _resize(self) -> None:
        self.capacity = len(self.buckets)
        new_capacity = self.capacity * 2
        old_buckets = self.buckets
        new_buckets = [[] for _ in range(new_capacity)]
        for bucket in old_buckets:
            if bucket:
                for hh, k, v in bucket:
                    node = (hh, k, v)
                    new_idx = hh % new_capacity
                    new_buckets[new_idx].append(node)
                self.buckets = new_buckets
                self.capacity = new_capacity
