from typing import Any


class Dictionary:
    def __init__(self, capacity: int = 8) -> None:
        self.capacity = capacity
        self.table = [[] for _ in range(capacity)]
        self.size = 0

    def __setitem__(self, key: Any, value: Any) -> None:
        key_hash = hash(key)
        index = key_hash % self.capacity
        bucket = self.table[index]

        for i, (k, v, h) in enumerate(bucket):
            if h == key_hash and k == key:
                bucket[i] = (key, value, key_hash)
                return

        bucket.append((key, value, key_hash))
        self.size += 1

    def __getitem__(self, key: Any) -> Any:
        key_hash = hash(key)
        index = key_hash % self.capacity
        bucket = self.table[index]

        for k, v, h in bucket:
            if h == key_hash and k == key:
                return v

        raise KeyError(key)

    def __len__(self) -> int:
        return self.size
