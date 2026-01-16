from typing import Any


class Node:
    def __init__(
            self,
            key: Any,
            value: Any,
            hash_value: int
    ) -> None:
        self.key = key
        self.value = value
        self.hash = hash_value


class Dictionary:
    def __init__(
            self,
            initial_capacity: int = 8,
            load_factor: float = 0.75
    ) -> None:
        self._size = 0
        self._capacity = initial_capacity
        self._load_factor = load_factor
        self._table = [[] for _ in range(self._capacity)]

    def _get_hash(self, key: Any) -> int:
        return hash(key)

    def _index(self, key: Any) -> int:
        return self._get_hash(key) % self._capacity

    def _resize(self) -> None:
        old_table = self._table
        self._capacity *= 2
        self._table = [[] for _ in range(self._capacity)]
        self._size = 0
        for bucket in old_table:
            for node in bucket:
                self[node.key] = node.value

    def __setitem__(self, key: Any, value: Any) -> None:
        if self._size + 1 > self._capacity * self._load_factor:
            self._resize()
        idx = self._index(key)
        bucket = self._table[idx]
        for node in bucket:
            if node.key == key:
                node.value = value
                return
        node = Node(key, value, self._get_hash(key))
        bucket.append(node)
        self._size += 1

    def __getitem__(self, key: Any) -> Any:
        idx = self._index(key)
        bucket = self._table[idx]
        for node in bucket:
            if node.key == key:
                return node.value
        raise KeyError(f"Key '{key}' not found")

    def __len__(self) -> int:
        return self._size
