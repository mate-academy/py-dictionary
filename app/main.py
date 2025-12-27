from __future__ import annotations
from typing import Any, Iterator
from math import floor


class Node:
    def __init__(self, key: Any, key_hash: int, value: Any) -> None:
        self.key = key
        self.key_hash = key_hash
        self.value = value

    def __repr__(self) -> str:
        return f"{self.key}: {self.value}"


class Dictionary:

    def __init__(self) -> None:
        self.size = 0
        self.capacity = 8
        self.load_factor = 2 / 3
        self.hash_table = [None] * self.capacity

    def hash_function(self, key_hash: int) -> int:
        return key_hash % self.capacity

    def find_index(self, key: Any) -> int:
        key_hash = hash(key)
        index = self.hash_function(key_hash)
        start_index = index

        if self.hash_table[index] is None or self.hash_table[index].key == key:
            return index

        while True:
            if (self.hash_table[index] is None
                    or self.hash_table[index].key == key):
                return index
            index = (index + 1) % self.capacity
            if index == start_index:
                raise KeyError(f"Key {key} not found.")

    def resize(self) -> None:
        temp = self.hash_table
        self.capacity *= 2
        self.hash_table = [None] * self.capacity
        self.size = 0

        for item in temp:
            if item is not None:
                self[item.key] = item.value

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.size == floor(self.capacity * self.load_factor):
            self.resize()

        key_hash = hash(key)
        index = self.find_index(key)

        if self.hash_table[index] is None:
            self.size += 1

        self.hash_table[index] = Node(key, key_hash, value)

    def __getitem__(self, key: Any) -> Any:
        index = self.find_index(key)
        item = self.hash_table[index]

        if item is None:
            raise KeyError(f"Key {key} not found.")

        return item.value

    def __len__(self) -> int:
        return self.size

    def __repr__(self) -> str:
        item_list = []
        for item in self.hash_table:
            if item is not None:
                item_list.append(f"{item.key}: {item.value}")
        return "{" + ", ".join(item_list) + "}"

    def clear(self) -> None:
        default_capacity = 8
        self.hash_table = [None] * default_capacity
        self.size = 0

    def __delitem__(self, key: Any) -> None:
        index = self.find_index(key)
        self.hash_table[index] = None
        self.size -= 1

    def get(self, key: Any, default: Any = None) -> Any:
        index = self.find_index(key)
        item = self.hash_table[index]

        if item is None:
            return default

        return item.value

    def pop(self, key: Any, value: Any = None) -> Any:
        index = self.find_index(key)
        item = self.hash_table[index]

        if item is None:
            if value is None:
                raise KeyError(f"Key {key} not found.")
            else:
                return value

        self.hash_table[index] = None
        self.size -= 1
        return item.value

    def update(self, iterable: Dictionary) -> None:
        if isinstance(iterable, Dictionary):
            for item in iterable.hash_table:
                if item is not None:
                    self[item.key] = item.value
        else:
            raise TypeError(
                "Iterable must be an instance of Dictionary class."
            )

    def __iter__(self) -> Iterator:
        for item in self.hash_table:
            if item is not None:
                yield item
