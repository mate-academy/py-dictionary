from collections.abc import Hashable
from fractions import Fraction
from typing import Any


class Dictionary:
    INITIAL_CAPACITY = 8
    LOAD_FACTOR = Fraction(2, 3)

    class Node:
        def __init__(self, key: Hashable, value: Any) -> None:
            self.key = key
            self.value = value
            self.hash = hash(key)

    def __init__(self) -> None:
        self.load_factor = self.LOAD_FACTOR
        self.capacity = self.INITIAL_CAPACITY
        self.size = 0
        self.table = [None] * self.capacity

    def _hash(self, key: Hashable) -> int:
        return hash(key) % self.capacity

    def _resize(self) -> None:
        old_table = self.table
        self.capacity *= 2
        self.table = [None] * self.capacity
        self.size = 0

        for node in old_table:
            if node is not None:
                self.__setitem__(node.key, node.value)

    def _insert(self, key: Hashable, value: Any) -> None:
        index = self._hash(key)
        while self.table[index] is not None:
            if self.table[index].key == key:
                self.table[index].value = value
                return
            index = (index + 1) % self.capacity
        self.table[index] = self.Node(key, value)
        self.size += 1

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.size >= self.capacity * self.load_factor:
            self._resize()
        self._insert(key, value)

    def __getitem__(self, key: Hashable) -> Any:
        index = self._hash(key)
        while self.table[index] is not None:
            if self.table[index].key == key:
                return self.table[index].value
            index = (index + 1) % self.capacity
        raise KeyError(f"Key '{key}' not found")

    def __len__(self) -> int:
        return self.size
