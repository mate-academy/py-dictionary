from __future__ import annotations
from dataclasses import dataclass
from typing import Hashable, Any


@dataclass
class Node:
    key: Hashable
    hash_key: int
    value: Any


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.capacity = 8
        self.load_factor = 2 / 3
        self.hash_table: list = [None] * self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        hash_key = hash(key)
        index = hash_key % self.capacity

        while True:
            if self.hash_table[index] is None:
                self.length += 1

                if self.length > self.capacity * self.load_factor:
                    self._resize(key, value)
                else:
                    self.hash_table[index] = Node(key, hash_key, value)
                return

            if self.hash_table[index].key == key:
                self.hash_table[index].value = value
                return

            index = (index + 1) % self.capacity

    def __getitem__(self, key: Hashable) -> Dictionary:
        while True:
            hash_key = hash(key)
            index = hash_key % self.capacity

            while True:
                if self.hash_table[index] is None:
                    raise KeyError(key)
                if self.hash_table[index].key == key:
                    return self.hash_table[index].value

                index = (index + 1) % self.capacity

    def __len__(self) -> int:
        return self.length

    def _resize(self, new_key: Hashable, new_value: Any) -> None:
        hash_table_temp = self.hash_table
        self.capacity *= 2
        self.hash_table = [None] * self.capacity
        self.length = 0

        for node in hash_table_temp:
            if node is not None:
                self.__setitem__(node.key, node.value)

        self.__setitem__(new_key, new_value)

    def clear(self) -> None:
        self.length = 0
        self.capacity = 8
        self.hash_table = [None] * self.capacity
