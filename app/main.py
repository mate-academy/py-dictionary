from dataclasses import dataclass
from typing import Hashable, Any

CAPACITY = 8
LOADER = 2 / 3


@dataclass
class Node:
    key: Hashable
    value: Any


class Dictionary:
    def __init__(self) -> None:
        self.hash_table: list[None | Node] = [None] * CAPACITY
        self.new_hash_table: list[None | Node] = []
        self.size = 0
        self.capacity = CAPACITY

    def __getitem__(self, item: Hashable) -> Any:
        index = self._calculate_index(item)

        if self.hash_table[index] is None:
            raise KeyError(f"Key '{item}' doesn't exist is dictionary")

        return self.hash_table[index].value

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self._calculate_index(key)

        if self.hash_table[index] is None:
            self.size += 1

        self.hash_table[index] = Node(key, value)

        if self.size >= (self.capacity * LOADER):
            self.resize()

    def _calculate_index(self, key: Hashable) -> int:
        index = hash(key) % self.capacity

        while (
                self.hash_table[index] is not None
                and self.hash_table[index].key != key
        ):
            index = (index + 1) % self.capacity

        return index

    def resize(self) -> None:
        self.capacity *= 2
        temp_table = self.hash_table.copy()

        self.hash_table = [None] * self.capacity

        for element in temp_table:
            if element is not None:
                index = self._calculate_index(element.key)
                self.hash_table[index] = Node(element.key, element.value)

        temp_table.clear()

    def __str__(self) -> str:
        return str(self.hash_table)

    def __len__(self) -> int:
        return self.size
