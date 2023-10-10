import dataclasses
from typing import Any
import math


@dataclasses.dataclass
class Node:
    key: Any
    value: Any


class Dictionary:
    INITIAL_CAPACITY = 8
    THRESHOLD = 2 / 3
    RESIZE_MULTIPLIER = 2

    def __init__(self):
        self.size = 0
        self.capacity = Dictionary.INITIAL_CAPACITY
        self.hash_table: list[Node | None] = [None] * self.capacity

    def __setitem__(self, key, value):
        table_index = hash(key) % self.capacity

        while self.hash_table[table_index] is not None:
            if self.hash_table[table_index].key == key:
                self.hash_table[table_index].value = value
                return

            table_index = (table_index + 1) % self.capacity

        if self.size >= math.floor(self.capacity * Dictionary.THRESHOLD):
            self._resize_hash_table()
            self.__setitem__(key=key, value=value)
            return

        self.size += 1
        self.hash_table[table_index] = Node(key=key, value=value)

    def _resize_hash_table(self):
        self.capacity *= Dictionary.RESIZE_MULTIPLIER
        nodes = [el for el in self.hash_table if el is not None]

        new_hash_table = [None] * self.capacity
        self.size = 0
        self.hash_table = new_hash_table

        for node in nodes:
            self.__setitem__(node.key, node.value)

    def __getitem__(self, item):
        table_index = hash(item) % self.capacity

        while self.hash_table[table_index] is not None:
            if self.hash_table[table_index].key == item:
                return self.hash_table[table_index].value

            table_index = (table_index + 1) % self.capacity

        raise KeyError(f"Key {item} does not exist in Dictionary!")

    def __len__(self):
        return len([el for el in self.hash_table if el is not None])
