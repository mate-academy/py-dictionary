from typing import Any, Optional


class Dictionary:
    def __init__(self, initial_capacity: int = 8) -> None:
        self._capacity: int = initial_capacity
        self._size: int = 0
        self._table: list[Optional[Dictionary._Node]] = [None] * self._capacity

    class _Node:
        def __init__(self, key: Any, value: Any, hash_value: int) -> None:
            self.key: Any = key
            self.value: Any = value
            self.hash: int = hash_value

    def _hash(self, key: Any) -> int:
        return hash(key) % self._capacity

    def _resize(self) -> None:
        old_table = self._table
        self._capacity *= 2
        self._table = [None] * self._capacity
        self._size = 0

        for node in old_table:
            if node is not None:
                self.__setitem__(node.key, node.value)

    def __setitem__(self, key: Any, value: Any) -> None:
        if self._size / self._capacity >= 0.7:  # Resize when load factor > 0.7
            self._resize()

        hash_value = self._hash(key)
        while self._table[hash_value] is not None:
            if self._table[hash_value].key == key:
                self._table[hash_value].value = value
                return
            hash_value = (hash_value + 1) % self._capacity

        self._table[hash_value] = self._Node(key, value, hash_value)
        self._size += 1

    def __getitem__(self, key: Any) -> Any:
        hash_value = self._hash(key)
        for _ in range(self._capacity):
            if self._table[hash_value] is None:
                break
            if self._table[hash_value].key == key:
                return self._table[hash_value].value
            hash_value = (hash_value + 1) % self._capacity

        raise KeyError(f"Key {key} not found.")

    def __len__(self) -> int:
        return self._size
