from dataclasses import dataclass
from typing import Hashable, Any


@dataclass
class Node:
    key: Hashable
    hash_value: int
    value: Any


class Dictionary:
    INITIAL_CAPACITY = 8
    LOAD_FACTOR = 2 / 3

    def __init__(self) -> None:
        self.capacity = self.INITIAL_CAPACITY
        self.size = 0
        self.table = [None] * self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.size + 1 > self.capacity * self.LOAD_FACTOR:
            self._resize()

        h = hash(key)
        index = self._calculate_index(key, h)
        while True:
            node = self.table[index]
            if node is None:
                self.table[index] = Node(key, h, value)
                self.size += 1
                return
            elif node.key == key:
                node.value = value
                return
            else:
                index = self._linear_probing(index)

    def __getitem__(self, key: Hashable) -> Any:
        h = hash(key)
        index = self._calculate_index(key, h)
        node = self.table[index]
        if node is None or node.key != key:
            raise KeyError(key)
        return node.value

    def __len__(self) -> int:
        return self.size

    def _resize(self) -> None:
        old_table = self.table
        self.capacity *= 2
        self.table = [None] * self.capacity
        self.size = 0
        for node in old_table:
            if node is not None:
                self[node.key] = node.value

    def _calculate_index(self, key: Hashable, hash_value: int) -> int:
        index = hash_value % self.capacity
        while (
                (node := self.table[index]) is not None
                and (hash_value != node.hash_value or key != node.key)
        ):
            index = self._linear_probing(index)
        return index

    def _linear_probing(self, index: int) -> int:
        return (index + 1) % self.capacity
