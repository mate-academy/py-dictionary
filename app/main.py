from dataclasses import dataclass
from typing import Hashable, Any


@dataclass
class Node:
    hash_value: int
    key: Hashable
    value: Any


class Dictionary:

    def __init__(self, capacity: int = 8) -> object:
        self.capacity = capacity
        self.factor = 2 / 3
        self.size = 0
        self.hash_table: list[Node | None] = [None] * self.capacity

    def __setitem__(self, key: object, value: object) -> object:
        if self.factor_is_reached():
            self.resize()
        self.add_pairs_to_hash_table(key, value)

    def __getitem__(self, key: Hashable) -> None:
        index = self.find_index(key)
        if self.is_cell_empty(index):
            raise KeyError(f"There is no key {key} in the hash table")
        return self.hash_table[index].value

    def find_index(self, key: Hashable) -> int:
        hash_value = hash(key)
        index = hash_value % self.capacity

        while (
                self.hash_table[index] is not None
                and (
                    self.hash_table[index].hash_value != hash_value
                    or self.hash_table[index].key != key
                )
        ):
            index += 1
            index %= self.capacity
        return index

    def __len__(self) -> int:
        return self.size

    def resize(self) -> None:
        self.capacity *= 2
        old_table = self.hash_table
        self.hash_table = [None] * self.capacity
        self.size = 0

        for item in old_table:
            if item is not None:
                self.__setitem__(item.key, item.value)

    def factor_is_reached(self) -> bool:
        return self.size >= self.capacity * self.factor

    def is_cell_empty(self, cell_index: int) -> None:
        return self.hash_table[cell_index] is None

    def add_pairs_to_hash_table(self, key: int, value: any) -> None:
        index = self.find_index(key)

        if self.is_cell_empty(index):
            self.size += 1

        self.hash_table[index] = Node(hash(key), key, value)
