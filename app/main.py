from typing import Any


class Dictionary:
    def __init__(self, initial_capacity: int = 8) -> None:
        self.capacity: int = initial_capacity
        self.size: int = 0
        self.table: list[list[tuple[Any, int, Any]]] = [
            [] for _ in range(self.capacity)
        ]

    def __setitem__(self, key: Any, value: Any) -> None:
        node_hash: int = hash(key)
        index: int = node_hash % self.capacity
        bucket = self.table[index]

        for i, (k, h, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, h, value)
                return
        bucket.append((key, node_hash, value))
        self.size += 1

        if self.size / self.capacity > 0.7:
            self._resize()

    def __getitem__(self, key: Any) -> Any:
        node_hash: int = hash(key)
        index: int = node_hash % self.capacity
        bucket = self.table[index]

        for k, h, v in bucket:
            if k == key:
                return v
        raise KeyError(f"Key {key} not found")

    def __len__(self) -> int:
        return self.size

    def _resize(self) -> None:
        old_table = self.table
        self.capacity *= 2
        self.table = [[] for _ in range(self.capacity)]
        self.size = 0
        for bucket in old_table:
            for k, h, v in bucket:
                self[k] = v
