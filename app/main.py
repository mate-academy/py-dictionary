from __future__ import annotations
from typing import Hashable, Any
from dataclasses import dataclass


@dataclass
class Node:
    key: Hashable
    value: Any
    hash_el: int


class Dictionary:
    INITIAL_CAPACITY = 8
    THRESHOLD = 2 / 3
    CAPACITY_MULTIPLIER = 2

    def __init__(self, capacity: int = INITIAL_CAPACITY) -> None:
        self.capacity = capacity
        self.size = 0
        self.hash_table: list[None | Node] = [None] * self.capacity

    def _linear_probing(self, index: int) -> int:
        return (index + 1) % self.capacity

    def _calculate_index(self, key: Hashable) -> int:
        key_hash = hash(key)
        index = key_hash % self.capacity
        while (node := self.hash_table[index]) is not None:
            if node.key == key and node.hash_el == key_hash:
                break
            index = self._linear_probing(index)
        return index

    def _resize(self) -> None:
        old_hash_table = self.hash_table
        self.capacity *= self.CAPACITY_MULTIPLIER
        self.hash_table = [None] * self.capacity
        self.size = 0
        for node in old_hash_table:
            if node is not None:
                self.__setitem__(node.key, node.value)

    def __setitem__(self, key: Hashable, value: Any) -> None:
        node = Node(key, value, hash(key))
        index = self._calculate_index(key)
        if self.hash_table[index] is None:
            self.size += 1
        self.hash_table[index] = node
        if self.size >= self.THRESHOLD * self.capacity:
            self._resize()

    def __getitem__(self, key: Hashable) -> None:
        index = self._calculate_index(key)
        if self.hash_table[index] is not None:
            return self.hash_table[index].value
        raise KeyError(f"key: {key} not found")

    def __len__(self) -> int:
        return self.size

    def __str__(self) -> str:
        return " ".join(str(node.value) for node
                        in self.hash_table if node is not None)

    def __repr__(self) -> str:
        return str(self)
