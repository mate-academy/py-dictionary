from typing import Any, Hashable
from dataclasses import dataclass


@dataclass
class Node:
    key: Hashable
    value: Any
    key_hash: int


class Dictionary:
    def __init__(self, initial_capacity: int = 8) -> None:
        self.capacity = initial_capacity
        self.size = 0
        self.table = [None] * self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.size / self.capacity >= 0.7:
            self._resize()
        node = Node(key, value, hash(key))
        index = node.key_hash % self.capacity
        if self.table[index] is None:
            self.table[index] = []
        for item in self.table[index]:
            if item.key == key:
                item.value = value
                return
        self.table[index].append(node)
        self.size += 1

    def __getitem__(self, key: Hashable) -> Any:
        index = hash(key) % self.capacity
        if self.table[index] is not None:
            for item in self.table[index]:
                if item.key == key:
                    return item.value
        raise KeyError(f"Key {key} not found")

    def __len__(self) -> int:
        return self.size

    def _resize(self) -> None:
        new_capacity = self.capacity * 2
        new_table = [None] * new_capacity
        for i in range(self.capacity):
            if self.table[i] is not None:
                for node in self.table[i]:
                    index = node.key_hash % new_capacity
                    if new_table[index] is None:
                        new_table[index] = []
                    new_table[index].append(node)
        self.capacity = new_capacity
        self.table = new_table
