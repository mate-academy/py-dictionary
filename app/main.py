from typing import Hashable, Any
from dataclasses import dataclass


@dataclass
class Node:
    key: Hashable
    value: Any


class Dictionary:
    def __init__(self, capacity: int = 8, load_factor: float = 0.65) -> None:
        self.capacity = capacity
        self.load_factor = load_factor
        self.size = 0
        self.hash_table = [None] * self.capacity

    def _calculate_index(self, key: Hashable) -> int:
        index = hash(key) % self.capacity

        while (self.hash_table[index] is not None
               and self.hash_table[index].key != key):
            index = (index + 1) % self.capacity

        return index

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self._calculate_index(key)
        if self.hash_table[index] is None:
            self.size += 1
        self.hash_table[index] = Node(key, value)
        if self.size / self.capacity >= self.load_factor:
            self._resize()

    def __getitem__(self, key: Hashable) -> Any:
        index = self._calculate_index(key)
        if self.hash_table[index] is None:
            raise KeyError(key)
        return self.hash_table[index].value

    def __len__(self) -> int:
        return self.size

    def _resize(self) -> None:
        old_hash_table = self.hash_table
        self.capacity *= 2
        self.hash_table = [None] * self.capacity
        self.size = 0

        for node in old_hash_table:
            if node is not None:
                self.__setitem__(node.key, node.value)

    def __str__(self) -> str:
        return str(self.hash_table)
