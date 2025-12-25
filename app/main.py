from __future__ import annotations
from dataclasses import dataclass
from typing import Hashable, Any


@dataclass
class Node:
    key: Hashable
    value: Any
    _hash: int


class Dictionary:
    def __init__(self) -> None:
        self.capacity: int = 8
        self.hash_table: list = [None] * self.capacity
        self.load_factor: float = 2 / 3
        self.length: int = 0

    def __resize(self) -> None:
        self.capacity *= 8
        hash_table = self.hash_table
        self.hash_table = [None] * self.capacity
        self.length = 0
        for content in hash_table:
            if content:
                self.__setitem__(content.key, content.value)

    def __find_index(self, key: Hashable) -> int:
        _hash = hash(key)
        index = _hash % self.capacity
        while self.hash_table[index] and self.hash_table[index].key != key:
            index += 1
            index %= self.capacity
        return index

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.length + 1 >= self.capacity * self.load_factor:
            self.__resize()
        index = self.__find_index(key)
        if not self.hash_table[index]:
            self.hash_table[index] = Node(key, value, hash(key))
            self.length += 1
            return
        self.hash_table[index].value = value

    def __getitem__(self, key: Hashable) -> Any:
        index = self.__find_index(key)
        if self.hash_table[index]:
            return self.hash_table[index].value
        raise KeyError(f"No value for this key: {key}")

    def __len__(self) -> int:
        return self.length

    def clear(self) -> None:
        self.hash_table = [None] * self.capacity
        self.length = 0

    def __delitem__(self, key: Hashable) -> None:
        index = self.__find_index(key)
        self.hash_table[index] = None
        self.length -= 1

    def get(self, key: Hashable, value: Any = None) -> Any:
        index = self.__find_index(key)
        if self.hash_table[index]:
            if value == self.hash_table[index].value:
                return self.hash_table[index].value
        return None

    def pop(self, key: Hashable) -> Any:
        self.__delitem__(key)
        return self.__getitem__(key)

    def update(self, _dict: Dictionary) -> None:
        for content in _dict.hash_table:
            self.__setitem__(content.key, content.value)

    def __iter__(self) -> list:
        result = []
        for element in self.hash_table:
            result.append(element.key)
        return result
