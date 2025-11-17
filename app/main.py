from typing import Any, List


class Dictionary:
    def __init__(
        self,
        initial_capacity: int = 8,
        load_factor: float = 0.75
    ) -> None:
        self._capacity: int = initial_capacity
        self._load_factor: float = load_factor
        self._size: int = 0
        self._table: List[List[list]] = [
            [] for _ in range(initial_capacity)
        ]

    def _get_index(self, key_hash: int) -> int:
        return key_hash % self._capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        key_hash = hash(key)
        index = self._get_index(key_hash)
        bucket = self._table[index]

        for node in bucket:
            if node[0] == key:
                node[2] = value
                return

        bucket.append([key, key_hash, value])
        self._size += 1

        if self._size / self._capacity > self._load_factor:
            self._resize()

    def __getitem__(self, key: Any) -> Any:
        key_hash = hash(key)
        index = self._get_index(key_hash)
        bucket = self._table[index]

        for k, h, v in bucket:
            if k == key:
                return v

        raise KeyError(f"Key {key} not found")

    def __delitem__(self, key: Any) -> None:
        key_hash = hash(key)
        index = self._get_index(key_hash)
        bucket = self._table[index]

        for i, (k, h, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self._size -= 1
                return

        raise KeyError(f"Key {key} not found")

    def __len__(self) -> int:
        return self._size

    def clear(self) -> None:
        self._table = [[] for _ in range(self._capacity)]
        self._size = 0

    def _resize(self) -> None:
        old_table = self._table
        new_capacity = self._capacity * 2
        self._capacity = new_capacity
        self._table = [[] for _ in range(new_capacity)]
        self._size = 0

        for bucket in old_table:
            for key, key_hash, value in bucket:
                self[key] = value
