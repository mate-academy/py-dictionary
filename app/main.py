from random import randint
from typing import Any, Hashable
from dataclasses import dataclass


@dataclass
class Node:
    key: Hashable
    node_hash: int
    value: Any

    def set_value(self, value: Any) -> None:
        self.value = value


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.hash_table: list = [None] * 8
        self.load_capacity = (2 / 3)
        self.capacity = 8

    def rearrange_dict(self) -> None:

        old_dict = self.hash_table
        self.capacity *= 2
        self.hash_table = [None] * self.capacity

        for node in old_dict:
            if node:
                self.__setitem__(node.key, node.value)
                self.length -= 1

    def __setitem__(self, key: Hashable, value: Any) -> None:

        index = hash(key) % self.capacity

        if self.hash_table[index] is None:
            self.hash_table[index] = Node(key, hash(key), value)
            self.set_length()

        node_present = self.check_for_presence(key)
        if node_present:
            node_present.set_value(value)

        else:
            index = self.get_random_index(index)
            self.hash_table[index] = Node(key, hash(key), value)
            self.set_length()

        self.save_space()

    def __getitem__(self, key: Hashable) -> Any:
        node_present = self.check_for_presence(key)
        if node_present:
            return node_present.value

        else:
            raise KeyError(key)

    def __len__(self) -> int:
        return self.length

    def check_for_presence(self,
                           key: Hashable) -> Node | bool:

        index = hash(key) % self.capacity

        if (self.hash_table[index]
                and self.hash_table[index].key == key):
            return self.hash_table[index]

        for node in self.hash_table:

            if node and node.key == key:
                return node

        return False

    def save_space(self) -> None:
        free_space = self.capacity - self.capacity * self.load_capacity
        if self.hash_table.count(None) <= free_space:
            self.rearrange_dict()

    def get_random_index(self, index: int) -> int:
        while self.hash_table[index]:
            index = randint(0, self.capacity - 1)
        return index

    def set_length(self) -> None:
        self.length += 1
