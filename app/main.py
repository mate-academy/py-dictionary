from __future__ import annotations

from dataclasses import dataclass
from math import floor
from typing import Any, Hashable, Optional, List, Iterator


@dataclass
class Node:
    key: Hashable
    value: Any
    hash_of_node: int


class Dictionary:
    def __init__(self, capacity: int = 8, load_factor: float = 2 / 3) -> None:
        self.capacity = capacity
        self.load_factor = load_factor
        self.size = 0
        self.hash_table: List[Optional[Node]] = [None] * self.capacity

    def __len__(self) -> int:
        return self.size

    def clear(self) -> None:
        self.size = 0
        self.hash_table = [None] * self.capacity

    def _index_for_key(self, key: Hashable) -> int:
        index = hash(key) % self.capacity
        while not (self.hash_table[index] is None
                   or (self.hash_table[index].key == key
                       and self.hash_table[index].hash_of_node == hash(key))):
            index = (index + 1) % self.capacity
        return index

    def _resize(self) -> None:
        old_table = [node for node in self.hash_table if node]
        self.capacity *= 2
        self.clear()
        for node in old_table:
            self[node.key] = node.value

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.size >= floor(self.capacity * self.load_factor):
            self._resize()
        index = self._index_for_key(key)
        if self.hash_table[index]:
            self.hash_table[index].value = value
        else:
            self.hash_table[index] = Node(key, value, hash(key))
            self.size += 1

    def __getitem__(self, key: Hashable) -> Any:
        index = self._index_for_key(key)
        if self.hash_table[index]:
            return self.hash_table[index].value
        raise KeyError

    def __delitem__(self, key: Hashable) -> None:
        index = self._index_for_key(key)
        self.hash_table[index] = None
        self.size -= 1

    def get(self, key: Hashable, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: Hashable, default: Any = "No argument") -> Any:
        try:
            value = self[key]
            self.__delitem__(key)
            return value
        except KeyError:
            if default == "No argument":
                raise KeyError
            return default

    def update(self, other_dictionary: Dictionary) -> None:
        for node in other_dictionary.hash_table:
            if node:
                self[node.key] = node.value

    def __iter__(self) -> Iterator:
        hash_table_without_none = [node for node in self.hash_table if node]
        return iter(hash_table_without_none)
