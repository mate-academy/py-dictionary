from __future__ import annotations

from typing import Hashable, Any


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.table = [None] * self.capacity
        self.load_factor = 2 / 3
        self.size = 0

    def _resize(self) -> None:
        if self.size >= self.capacity * self.load_factor:
            self.capacity *= 2
            copy_table = self.table.copy()
            self.table: list = [None] * self.capacity
            self.size = 0

            for node in copy_table:
                if node:
                    self.__setitem__(node.key, node.value)

    def __setitem__(self, key: Hashable, value: Any) -> None:
        self._resize()
        hash_value = hash(key)
        index = hash_value % self.capacity
        node = self.table[index]

        while node:
            if node.key == key and node.hash_value == hash_value:
                node.value = value
                return
            else:
                index = (index + 1) % self.capacity
                node = self.table[index]
        self.table[index] = Node(key, hash_value, value)
        self.size += 1

    def __getitem__(self, key: Hashable) -> None:
        hash_value = hash(key)
        index = hash_value % self.capacity
        node = self.table[index]
        while node:
            if node.key == key and node.hash_value == hash_value:
                return node.value
            else:
                index = (index + 1) % self.capacity
                node = self.table[index]
        raise KeyError(key)

    def __len__(self) -> int:
        return self.size


class Node:
    def __init__(self, key: Any, hash_value: Any, value: Any) -> None:
        self.key = key
        self.hash_value = hash_value
        self.value = value
