from __future__ import annotations

from typing import Hashable


class Dictionary:
    def __init__(
            self
    ) -> None:
        self.capacity = 8
        self.length = 0
        self.load_kef = (2 / 3)
        self.hash_table: list = [None] * self.capacity

    def get_index(self, key: Hashable) -> object:
        index = hash(key) % self.capacity
        while self.hash_table[index] and self.hash_table[index][0] != key:
            index = (index + 1) % self.capacity
        return index

    def __len__(self) -> int:
        return self.length

    def resize(self) -> None:
        self.capacity *= 2
        old_hash_table = self.hash_table
        self.hash_table = [None] * self.capacity
        self.length = 0
        for item in old_hash_table:
            if item is not None:
                self[item[0]] = item[2]

    def __setitem__(self, key: Hashable, value: object) -> None:
        index = self.get_index(key)
        if not self.hash_table[index]:
            if self.capacity * self.load_kef < self.length:
                self.resize()
                index = self.get_index(key)
            self.length += 1
        self.hash_table[index] = (key, hash(key), value)

    def __getitem__(self, key: Hashable) -> object:
        index = self.get_index(key)
        if not self.hash_table[index]:
            raise KeyError
        return self.hash_table[index][2]

    def __iter__(self) -> iter:
        return iter(self.hash_table)

    def __delitem__(self, key: Hashable) -> None:
        self.hash_table[hash(key) % len(self.hash_table)] = None

    def clear(self) -> None:
        self.hash_table = [None] * self.capacity
