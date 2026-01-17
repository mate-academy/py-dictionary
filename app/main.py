from typing import Hashable, Any
from dataclasses import dataclass


@dataclass
class Node:
    key: Hashable
    key_hash: int
    value: Any


class Dictionary:
    LOAD_FACTOR = 2 / 3

    def __init__(self) -> None:
        self.size = 0
        self.capacity = 8
        self.hash_table: list = [None] * self.capacity

    def resize_table(self) -> None:
        self.size = 0
        self.capacity *= 2
        old_hash_table = self.hash_table
        self.hash_table = [None] * self.capacity

        for node in old_hash_table:
            if node:
                self.__setitem__(node.key, node.value)

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.size >= self.LOAD_FACTOR * self.capacity:
            self.resize_table()

        index = hash(key) % self.capacity

        while True:
            if not self.hash_table[index]:
                self.hash_table[index] = Node(key, hash(key), value)
                self.size += 1
                break
            if self.hash_table[index].key == key:
                self.hash_table[index].value = value
                break
            index = (index + 1) % self.capacity

    def __getitem__(self, key: Hashable) -> Any:
        index = hash(key) % self.capacity

        while self.hash_table[index]:
            if self.hash_table[index].key == key:
                return self.hash_table[index].value
            index = (index + 1) % self.capacity
        raise KeyError

    def __len__(self) -> int:
        return self.size
