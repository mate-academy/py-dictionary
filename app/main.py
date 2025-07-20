from dataclasses import dataclass
from typing import Hashable, Any


@dataclass
class Node:
    key: Hashable
    hash: int
    value: Any


class Dictionary:
    INITIAL_CAPACITY = 8
    LOAD_FACTOR = 2 / 3

    def __init__(self) -> None:
        self.capacity = self.INITIAL_CAPACITY
        self.size = 0
        self.table = [None] * self.INITIAL_CAPACITY

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.size + 1 > self.capacity * self.LOAD_FACTOR:
            self._resize()

        index = self._calculate_index(key)

        if (node := self.table[index]) is None:
            self.table[index] = Node(key, hash(key), value)
            self.size += 1
        else:
            node.value = value

    def _calculate_index(self, key: Hashable) -> int:
        hash_value = hash(key)
        index = hash_value % self.capacity
        while (
                (node := self.table[index]) is not None
                and (hash_value != node.hash or key != node.key)
        ):
            index = self._linear_probing(index)
        return index

    def __getitem__(self, key):
        index = self._calculate_index(key)
        if (node := self.table[index]) is None:
            raise KeyError
        return node.value


    def __len__(self):
        return self.size


    def _resize(self) -> None:
        old_table = self.table
        self.capacity *= 2
        self.table = [None] * self.capacity
        self.size = 0
        for node in old_table:
            if node is not None:
                self[node.key] = node.value


    def _linear_probing(self, index: int) -> int:
        return (index + 1) % self.capacity
