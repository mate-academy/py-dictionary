from typing import Hashable, Any
from dataclasses import dataclass


@dataclass
class Node:
    key: Hashable
    value: Any


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.capacity = 8
        self.load_factor = 0.66
        self.increaser = 2
        self.hash_table: list = [None] * self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        new_node = Node(key, value)
        index = hash(new_node.key) % self.capacity

        while self.hash_table[index]:
            if self.hash_table[index].key == key:
                self.hash_table[index] = new_node
                return

            index = (index + 1) % self.capacity

        if self.length + 1 > self.capacity * self.load_factor:
            self.__resize()
            self.__setitem__(key, value)
            return

        self.length += 1

        self.hash_table[index] = new_node

    def __getitem__(self, key: Hashable) -> Any:
        key_hash = hash(key)
        index = key_hash % self.capacity

        while self.hash_table[index] and self.hash_table[index].key != key:
            index = (index + 1) % self.capacity

        if not self.hash_table[index]:
            raise KeyError(f"{key} does not exist")

        return self.hash_table[index].value

    def __resize(self) -> None:
        old_hash_table = self.hash_table
        self.length = 0
        self.capacity *= self.increaser
        self.hash_table = [None] * self.capacity

        for item in old_hash_table:
            if item:
                self.__setitem__(item.key, item.value)

    def __len__(self) -> int:
        return self.length

    def __str__(self) -> str:
        return str(self.hash_table)
