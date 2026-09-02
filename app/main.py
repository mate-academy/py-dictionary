from dataclasses import dataclass
from typing import Hashable, Any


@dataclass
class Node:
    key: Hashable
    value: Any
    key_hash: int

    def __init__(self, key: Hashable, value: Any) -> None:
        self.key = key
        self.value = value
        self.key_hash = hash(key)


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.load_factor = 2 / 3
        self.capacity = 8
        self.hash_table: list = [None] * self.capacity

    def resize(self) -> None:
        old_hash_table = self.hash_table
        self.capacity *= 2
        self.hash_table = [None] * self.capacity
        self.length = 0

        for node in old_hash_table:
            if node is not None:
                self.__setitem__(node.key, node.value)

    def __setitem__(self, key: Hashable, value: Any) -> None:
        element = Node(key, value)
        index = element.key_hash % self.capacity

        while self.hash_table[index] is not None:
            node = self.hash_table[index]
            if node.key_hash == element.key_hash and node.key == element.key:
                node.value = value
                return
            index = (index + 1) % self.capacity

        self.hash_table[index] = Node(key, value)
        self.length += 1

        if self.length > self.load_factor * self.capacity:
            self.resize()

    def __getitem__(self, key: Hashable) -> Any:
        key_hash = hash(key)
        index = key_hash % self.capacity
        while self.hash_table[index] is not None:
            node = self.hash_table[index]
            if node.key_hash == key_hash and node.key == key:
                return node.value
            index = (index + 1) % self.capacity

        raise KeyError(f"Key {key} not found")

    def __len__(self) -> int:
        return self.length

    def __delitem__(self, key: Hashable) -> None:
        key_hash = hash(key)
        index = key_hash % self.capacity
        while self.hash_table[index] is not None:
            node = self.hash_table[index]
            if node.key_hash == key_hash and node.key == key:
                self.hash_table[index] = None
                self.length -= 1
                return
            index = (index + 1) % self.capacity
