from typing import Any


class Dictionary:

    INITIAL_CAPACITY = 8
    LOAD_FACTOR = 0.75

    def __init__(self) -> None:
        self.capacity = self.INITIAL_CAPACITY
        self.size = 0
        self.table = [[] for _ in range(self.capacity)]

    def _hash(self, key: Any) -> int:
        return hash(key) % self.capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        index = self._hash(key)
        bucket = self.table[index]

        for i, (k, h, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, h, value)
                return

        bucket.append((key, hash(key), value))
        self.size += 1

        if self.size / self.capacity > self.LOAD_FACTOR:
            self._resize()

    def __getitem__(self, key: Any) -> Any:
        index = self._hash(key)
        bucket = self.table[index]

        for k, h, v in bucket:
            if k == key:
                return v

        raise KeyError(f"Key {key} not found")

    def __len__(self) -> int:
        return self.size

    def _resize(self) -> None:
        new_capacity = self.capacity * 2
        new_table = [[] for _ in range(new_capacity)]

        for bucket in self.table:
            for key, h, value in bucket:
                new_index = h % new_capacity
                new_table[new_index].append((key, h, value))

        self.capacity = new_capacity
        self.table = new_table
