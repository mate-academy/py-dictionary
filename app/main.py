from dataclasses import dataclass
from typing import Hashable, Any

INITIAL_CAPACITY = 8
RESIZE_THRESHOLD = 2 / 3
CAPACITY_MULTIPLIER = 2


@dataclass
class Node:
    key: Hashable
    value: Any


# O(1)
class Dictionary:
    def __init__(self, capacity: int = INITIAL_CAPACITY) -> None:
        self.capacity = capacity
        self.hash_table: list[Node | list | None] = [None] * self.capacity
        self.size = 0

    @property
    def current_max_size(self) -> float:
        return RESIZE_THRESHOLD * self.capacity

    def _calculate_index(self, key: Hashable) -> int:
        index = hash(key) % self.capacity
        while (self.hash_table[index]
               and self.hash_table[index].key != key):
            index = self._cyclic_increment(index)
        return index

    def _cyclic_increment(self, index: int) -> int:
        return (index + 1) % self.capacity

    def __getitem__(self, key: Hashable) -> Any:
        index = self._calculate_index(key)

        if self.hash_table[index] is None:
            raise KeyError(f"Cannot find value for key: {key}")

        return self.hash_table[index].value

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self._calculate_index(key)

        if self.hash_table[index] is None:
            if self.size + 1 >= self.current_max_size:
                self.resize()
                return self.__setitem__(key, value)

            self.size += 1

        self.hash_table[index] = Node(key, value)

    def resize(self) -> None:
        old_hash_table = self.hash_table

        self.__init__(self.capacity * 2)

        for node in old_hash_table:
            if node:
                self.__setitem__(node.key, node.value)

    def __str__(self) -> str:
        return str(self.hash_table)

    def __len__(self) -> int:
        return self.size
