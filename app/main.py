from typing import Hashable, Any
from dataclasses import dataclass

INITIAL_CAPACITY = 8


@dataclass
class Node:
    key: Hashable
    dict_hash: int
    value: Any


class Dictionary:
    def __init__(self, capacity: int = INITIAL_CAPACITY) -> None:
        self.capacity = capacity
        self.length = 0
        self.threshold = 2 / 3
        self.hash_table: list[Node | None] = [None] * self.capacity

    def __getitem__(self, key: Hashable) -> Any:
        index = self._calculation_index(key)

        if self.hash_table[index] is None:
            raise KeyError(f"Key {key} doesn't exist in dictionary")

        return self.hash_table[index].value

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.length / self.capacity > self.threshold:
            self._resize_hash_table()

        index = self._calculation_index(key)

        if (
                self.hash_table[index] is not None
                and self.hash_table[index].key == key
        ):
            self.hash_table[index].value = value
        else:
            self.length += 1
            self.hash_table[index] = Node(key, hash(key), value)

    def _calculation_index(self, key: Hashable) -> int:
        index = hash(key) % self.capacity

        while (
                self.hash_table[index] is not None
                and self.hash_table[index].key != key
        ):
            index = (index + 1) % self.capacity

        return index

    def _resize_hash_table(self) -> None:
        old_hash_table = self.hash_table
        new_size = self.capacity * 2

        self.hash_table = [None] * new_size
        self.capacity = new_size
        self.length = 0

        for node in old_hash_table:
            if node is not None:
                self.__setitem__(node.key, node.value)

    def __str__(self) -> str:
        return str(self.hash_table)

    def __len__(self) -> int:
        return self.length
