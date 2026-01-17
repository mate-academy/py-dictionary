from typing import Any, Hashable
from dataclasses import dataclass


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
        self.hash_table: list[None | Node] = [None] * self.INITIAL_CAPACITY

    def _resize(self) -> None:
        old_table = self.hash_table

        self.capacity *= 2
        self.hash_table = [None] * self.capacity
        self.size = 0

        for node in old_table:
            if node is not None:
                self[node.key] = node.value

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self._calculate_index(key)

        if (node := self.hash_table[index]) is None:
            if self.size + 1 > self.capacity * self.LOAD_FACTOR:
                self._resize()

                return self.__setitem__(key, value)

            self.hash_table[index] = Node(key, hash(key), value)
            self.size += 1
        else:
            node.value = value

    def __getitem__(self, key: Hashable) -> Any:
        index = self._calculate_index(key)

        if (node := self.hash_table[index]) is None:
            raise KeyError(key)
        else:
            return node.value

    def __len__(self) -> int:
        return self.size

    def _linear_probing(self, index: int) -> int:
        return (index + 1) % self.capacity

    def _calculate_index(self, key: Hashable) -> int:
        hash_value = hash(key)
        index = hash_value % self.capacity

        while (
                (node := self.hash_table[index]) is not None
                and (hash_value != node.hash_value or key != node.key)
        ):
            index = self._linear_probing(index)

        return index
