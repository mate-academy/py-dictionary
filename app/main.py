from __future__ import annotations
from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.hash_table: list = [[None, None] for _ in range(8)]
        self.capacity = 8

    def key_upp(self, key: int) -> int:
        return (key + 1) % self.capacity

    def write(self, index: int, key: Hashable, value: Any) -> None:
        self.hash_table[index][0] = key
        self.hash_table[index][1] = value

    def resize(self) -> None:
        self.capacity *= 2
        old_hash_table = self.hash_table
        self.hash_table = [[None, None] for _ in range(self.capacity)]
        self.length = 0
        for key, value in old_hash_table:
            if key:
                self.__setitem__(key, value)

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.length > self.capacity * 2 // 3:
            self.resize()

        index = hash(key) % self.capacity
        for _ in range(self.capacity):
            if self.hash_table[index][0] is None:
                self.write(index, key, value)
                self.length += 1
                break
            if self.hash_table[index][0] == key:
                self.write(index, key, value)
                break
            index = self.key_upp(index)

    def __getitem__(self, key: Hashable) -> Any:
        index = hash(key) % self.capacity
        for _ in range(self.capacity):
            if self.hash_table[index][0] == key:
                return self.hash_table[index][1]
            index = self.key_upp(index)
        raise KeyError

    def __len__(self) -> int:
        return self.length
