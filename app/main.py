from typing import Any, Hashable
from dataclasses import dataclass


@dataclass
class Node:
    key: Hashable
    value: Any


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.hash_table: list[None | Node] = [None] * self.capacity
        self.load_factor = 2 / 3
        self.threshold = int(self.capacity * self.load_factor)
        self.size = 0

    def _index(self, key: Hashable) -> int:
        index = hash(key) % self.capacity
        while (
            self.hash_table[index] is not None
            and self.hash_table[index].key != key
        ):
            index = (index + 1) % self.capacity
        return index

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.size == self.threshold:
            self._resize()

        index = self._index(key)

        if self.hash_table[index] is None:
            self.size += 1

        self.hash_table[index] = Node(key, value)

    def __getitem__(self, key: Hashable) -> Any:
        index = self._index(key)
        if self.hash_table[index] is None:
            raise KeyError("Not found")
        return self.hash_table[index].value

    def __len__(self) -> int:
        return self.size

    def _resize(self) -> None:
        old_table = self.hash_table
        self.size = 0
        self.capacity *= 2
        self.threshold = int(self.load_factor * self.capacity)
        self.hash_table = [None] * self.capacity

        for node in old_table:
            if node is not None:
                self.__setitem__(node.key, node.value)
