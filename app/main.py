from __future__ import annotations
from typing import Hashable, Any


class Node:
    def __init__(self, key: Hashable, hash_val: int, value: Any) -> None:
        self.key = key
        self.hash_val = hash_val
        self.value = value


def _is_matching_key(node: Node, key: Hashable) -> bool:
    return node.key == key and node.hash_val == hash(key)


class Dictionary:
    LOAD_FACTOR = 2 / 3

    def __init__(self) -> None:
        self.size = 0
        self.capacity: int = 8
        self.table: list = [None] * self.capacity

    def get_index(self, key: Hashable) -> int:
        index = hash(key) % self.capacity
        while (
                self.table[index] and not
                _is_matching_key(self.table[index], key)):
            index = (index + 1) % self.capacity
        return index

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.size >= self.capacity * self.LOAD_FACTOR:
            self.resize()
        index = self.get_index(key)
        if self.table[index]:
            self.table[index].value = value
        else:
            self.size += 1
            self.table[index] = Node(key, hash(key), value)

    def __getitem__(self, key: Hashable) -> Any:
        index = self.get_index(key)
        if self.table[index] and _is_matching_key(self.table[index], key):
            return self.table[index].value
        raise KeyError(key)

    def __len__(self) -> int:
        return self.size

    def resize(self) -> None:
        old_table = self.table
        self.capacity *= 2
        self.table = [None] * self.capacity
        self.size = 0
        for element in old_table:
            if element:
                self[element.key] = element.value

    def __delitem__(self, key: Hashable) -> None:
        index = self.get_index(key)
        if self.table[index] and _is_matching_key(self.table[index], key):
            self.table[index] = None
            self.size -= 1

    def clear(self) -> None:
        self.__init__()
