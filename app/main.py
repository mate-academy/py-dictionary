from dataclasses import dataclass
from typing import Any


@dataclass
class Node:
    key: Any
    hash: int  # noqa: VNE003
    value: Any


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.hash_table: list[Node | None] = [None] * 8

    def _find_slot(self, key: Any, key_hash: int) -> int:
        index = key_hash % len(self.hash_table)
        while self.hash_table[index] is not None:
            node = self.hash_table[index]
            if node.hash == key_hash and (node.key is key or node.key == key):
                return index
            index = (index + 1) % len(self.hash_table)
        return index

    def _resize(self) -> None:
        previous_table = self.hash_table
        self.hash_table = [None] * (2 * len(previous_table))
        for node in previous_table:
            if node is not None:
                index = self._find_slot(node.key, node.hash)
                self.hash_table[index] = node

    def __setitem__(self, key: Any, value: Any) -> None:
        key_hash = hash(key)
        index = self._find_slot(key, key_hash)
        node = self.hash_table[index]
        if node is not None:
            node.value = value
            return
        if (self.length + 1) * 3 > len(self.hash_table) * 2:
            self._resize()
            index = self._find_slot(key, key_hash)
        self.hash_table[index] = Node(key, key_hash, value)
        self.length += 1

    def __getitem__(self, key: Any) -> Any:
        key_hash = hash(key)
        node = self.hash_table[self._find_slot(key, key_hash)]
        if node is None:
            raise KeyError(key)
        return node.value

    def __len__(self) -> int:
        return self.length
