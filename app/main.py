from dataclasses import dataclass
from typing import Any


@dataclass
class Node:
    key: Any
    hash_code: int
    value: Any


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.hash_table: list = [None] * 8

    def capacity(self) -> int:
        return len(self.hash_table)

    def find_index(self, key: Any, hash_code: int) -> int:
        index = hash_code % self.capacity()
        while True:
            node = self.hash_table[index]
            if node is None or (
                node.hash_code == hash_code and node.key == key
            ):
                return index
            index = (index + 1) % self.capacity()

    def resize(self) -> None:
        prev_table = self.hash_table
        self.hash_table = [None] * (self.capacity() * 2)
        self.length = 0
        for node in prev_table:
            if node is not None:
                self.insert(node)

    def insert(self, node: Node) -> None:
        index = self.find_index(node.key, node.hash_code)
        if self.hash_table[index] is None:
            self.length += 1
        self.hash_table[index] = node

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.length / self.capacity() >= 2 / 3:
            self.resize()
        self.insert(Node(key, hash(key), value))

    def __getitem__(self, key: Any) -> Any:
        hash_code = hash(key)
        node = self.hash_table[self.find_index(key, hash_code)]
        if node is None:
            raise KeyError(f"Key {key} doesn't exist")
        return node.value

    def __len__(self) -> int:
        return self.length
