from __future__ import annotations
from typing import Hashable, Any


class Node:
    def __init__(self, key: Hashable, hash_val: int, value: Any) -> None:
        self.key = key
        self.hash_val = hash_val
        self.value = value


class Dictionary:
    LOAD_FACTOR = 2 / 3

    def __init__(self) -> None:
        self.size = 0
        self.capacity: int = 8
        self.table: list = [None] * self.capacity

    def get_index(self, key: Hashable) -> int:
        index = hash(key) % self.capacity
        while self.table[index] and self.table[index].key != key:
            index = (index + 1) % self.capacity
        return index

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.size >= self.capacity * self.LOAD_FACTOR:
            self.resize()
        index = self.get_index(key)
        while self.capacity <= index:
            self.resize()
        if self.table[index]:
            self.table[index].value = value
        else:
            self.size += 1
            node = Node(key, hash(key), value)
            self.table[index] = node

    def __getitem__(self, key: Hashable) -> Any:
        index = self.get_index(key)
        if len(self.table) > index:
            if self.table[index]:
                if self.table[index].key == key:
                    return self.table[index].value
            raise KeyError(key)
        else:
            raise IndexError

    def __len__(self) -> int:
        return self.size

    def resize(self) -> None:
        olf_table = self.table
        self.capacity *= 2
        self.table = [None] * self.capacity
        self.size = 0
        for element in olf_table:
            if element:
                self.__setitem__(element.key, element.value)

    def __delitem__(self, key: Hashable) -> None:
        index = self.get_index(key)
        if self.table[index]:
            self.table[index] = None
            self.size -= 1

    def get(self, item: Hashable) -> None:
        self.__getitem__(item)

    def clear(self) -> Dictionary:
        return self.__init__()
