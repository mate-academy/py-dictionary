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
        self._table: list[Node | None] = [None] * self._capacity

    def _find_slot(self, key: Any, key_hash: int) -> int:
        index = key_hash % self._capacity

        while self._table[index] is not None:
            node = self._table[index]

            if node.key_hash == key_hash and (
                node.key is key or node.key == key
            ):
                return index

            index = (index + 1) % self._capacity

        return index

    def _resize(self) -> None:
        old_table = self._table
        self._capacity *= 2
        self._table = [None] * self._capacity

        for node in old_table:
            if node is not None:
                index = self._find_slot(node.key, node.key_hash)
                self._table[index] = node

    def __setitem__(self, key: Any, value: Any) -> None:
        key_hash = hash(key)
        index = self._find_slot(key, key_hash)
        node = self._table[index]

        if node is not None:
            node.value = value
            return

        if (self._size + 1) * 3 > self._capacity * 2:
            self._resize()
            index = self._find_slot(key, key_hash)

        self._table[index] = Node(key, key_hash, value)
        self._size += 1

    def __getitem__(self, key: Any) -> Any:
        index = self._find_slot(key, hash(key))
        node = self._table[index]

        if node is None:
            raise KeyError(key)

        return node.value

    def __len__(self) -> int:
        return self._size
