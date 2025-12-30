from typing import Any


class Dictionary:

    LOAD_FACTOR = 0.75

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

        if self.size / self.capacity > self.LOAD_FACTOR:
            self._resize()

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

    def _resize(self) -> None:
        old_table = self.table
        self.capacity *= 2
        self.table = [[] for _ in range(self.capacity)]
        self.size = 0

        for bucket in old_table:
            for k, v, h in bucket:
                self[k] = v
