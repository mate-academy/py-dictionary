from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Hashable


@dataclass
class Node:
    key: Hashable
    hash_: int
    value: Any


class Dictionary:

    def __init__(self, capacity: int = 8) -> None:
        self.capacity = capacity
        self.threshold = int(self.capacity * (2 / 3)) + 1
        self.length = 0
        self.hash_table: list = [None] * self.capacity

    def __len__(self) -> int:
        return self.length

    def __setitem__(self, key: Hashable, value: Any) -> None:

        if self.length == self.threshold:
            self.resize()

        index = self.get_index(key)
        node = Node(key, hash(key), value)

        while self.hash_table[index] is not None:
            if self.hash_table[index].key == key:
                self.hash_table[index] = node
                return
            index = (index + 1) % self.capacity

        self.hash_table[index] = node
        self.length += 1

    def __getitem__(self, key: Any) -> Any:
        index = self.get_index(key)
        while self.hash_table[index] is not None:
            if self.hash_table[index].key == key:
                return self.hash_table[index].value
            index = (index + 1) % self.capacity
        raise KeyError

    def get_index(self, key: Hashable) -> int:
        return hash(key) % self.capacity

    def resize(self) -> None:
        old_hash_table = [item for item in self.hash_table if item is not None]
        self.__init__(self.capacity * 2)
        for item in old_hash_table:
            self.__setitem__(item.key, item.value)

    def clear(self) -> None:
        self.__init__()

    def __delitem__(self, key: Hashable) -> None:
        index = self.get_index(key)
        while self.hash_table[index] is not None:
            if self.hash_table[index].key == key:
                self.hash_table[index] = None
                self.length -= 1
                return
            index = (index + 1) % self.capacity

    def get(self, key: Hashable, value: Any = None) -> Any:
        index = self.get_index(key)
        while self.hash_table[index] is not None:
            if self.hash_table[index].key == key:
                return self.hash_table[index].value
            index = (index + 1) % self.capacity
        return value

    def pop(self, key: Hashable, value: Any = KeyError) -> Any:
        if self.get(key, value) == KeyError:
            raise KeyError
        return self.get(key, value)

    def update(self, other: Dictionary | list) -> Any:
        if type(other) is Dictionary:
            other_hash_table = [
                item for item in other.hash_table if item is not None
            ]
            for item in other_hash_table:
                self.__setitem__(item.key, item.value)
            return
        if type(other) is list and other:
            for item in other:
                self.__setitem__(item[0], item[1])
            return
        if type(other) is list and not other:
            return
        raise AttributeError
