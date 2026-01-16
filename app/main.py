from __future__ import annotations

from typing import Any, Hashable


class Node:
    def __init__(self, key: Hashable, value: Any) -> None:
        self.key = key
        self.hash_value = hash(self.key)
        self.value = value


class Dictionary:
    def __init__(self, capacity: int = 8) -> None:
        self.size = 0
        self.capacity = capacity
        self.load_factor = 2 / 3
        self.hash_table: list = [None] * self.capacity

    def get_index(self, key: Hashable) -> int:
        index = hash(key) % self.capacity
        while self.hash_table[index] and self.hash_table[index].key != key:
            index = (index + 1) % self.capacity
        return index

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.size >= self.capacity * self.load_factor:
            self.resize()

        index = self.get_index(key)
        while self.hash_table[index] and self.hash_table[index].key != key:
            index = (index + 1) % self.capacity

        if self.hash_table[index] and self.hash_table[index].key == key:
            self.hash_table[index].value = value
        else:
            node = Node(key, value)
            self.hash_table[index] = node
            self.size += 1

    def __getitem__(self, key: Hashable) -> Any:
        index = self.get_index(key)
        if self.hash_table[index] and self.hash_table[index].key == key:
            return self.hash_table[index].value
        raise KeyError("Key not found in the dictionary.")

    def resize(self) -> None:
        old_hash_table = self.hash_table.copy()
        self.size = 0
        self.capacity *= 2
        self.hash_table = [None] * self.capacity

        for node in old_hash_table:
            if node:
                self[node.key] = node.value

    def __len__(self) -> int:
        return self.size

    def __iter__(self) -> object:
        return self

    def __next__(self) -> Any:
        index = 0
        while index < self.capacity:
            if self.hash_table[index]:
                yield self.hash_table[index].value
            index += 1
        raise StopIteration("Dictionary index out of range.")

    def update(self, dictionary: Dictionary) -> None:
        for key, value in dictionary.items():
            self[key] = value

    def items(self) -> list:
        index = 0
        while index < self.capacity:
            if self.hash_table[index]:
                yield [self.hash_table[index].key,
                       self.hash_table[index].value]
            index += 1
        raise StopIteration("Dictionary index out of range.")

    def get(self, key: Hashable, value: Any = None) -> Any:
        index = self.get_index(key)
        if self.hash_table[index] and self.hash_table[index].key == key:
            return self.hash_table[index].value
        return value

    def pop(self, key: Hashable, value: Any = None) -> Any:
        index = self.get_index(key)
        if self.hash_table[index] and self.hash_table[index].key == key:
            value = self.hash_table[index].value
            self.hash_table[index] = None
            self.size -= 1
            return value
        return value

    def __delitem__(self, key: Hashable) -> None:
        index = self.get_index(key)
        if self.hash_table[index] and self.hash_table[index].key == key:
            self.hash_table[index] = None
            self.size -= 1

    def clear(self) -> Dictionary:
        return self.__init__()
