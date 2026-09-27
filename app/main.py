from dataclasses import dataclass
from typing import Any


@dataclass
class Node:
    key: Any
    key_hash: int
    value: Any


class Dictionary:
    def __init__(self) -> None:
        self._capacity = 8
        self._size = 0
        self._table = [None] * self._capacity

    def _resize(self) -> None:
        _table = self._table
        self._capacity *= 2
        self._table = [None] * self._capacity
        self._size = 0

        for node in _table:
            if node is not None:
                self.__setitem__(key=node.key, value=node.value)

    def __setitem__(self, key: Any, value: Any) -> None:
        key_hash = hash(key)
        index = key_hash % self._capacity

        for _ in range(self._capacity):
            node = self._table[index]

            if node is None:
                if self._capacity * 2 / 3 <= self._size + 1:
                    self._resize()
                    self.__setitem__(key=key, value=value)
                    return

                self._table[index] = Node(
                    key=key,
                    key_hash=key_hash,
                    value=value
                )
                self._size += 1
                return

            elif node.key_hash == key_hash and node.key == key:
                self._table[index] = Node(
                    key=key,
                    key_hash=key_hash,
                    value=value
                )
                return

            index = (index + 1) % self._capacity

    def __getitem__(self, key: Any) -> Any:
        key_hash = hash(key)
        index = key_hash % self._capacity

        for _ in range(self._capacity):
            node = self._table[index]
            if node is None:
                raise KeyError(f"Key '{key}' not found")
            if node.key_hash == key_hash and node.key == key:
                return node.value

            index = (index + 1) % self._capacity
        raise KeyError(f"Key '{key}' not found")

    def __len__(self) -> int:
        return self._size
