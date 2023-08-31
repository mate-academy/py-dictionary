from __future__ import annotations
from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self._capacity = 8
        self._load_factor = 0.67
        self._length = 0
        self._hash_table = [None] * self._capacity

    def __len__(self) -> int:
        return self._length

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self._length > self._capacity * self._load_factor:
            self.__resize()
        index = self.__index(key)
        if not self._hash_table[index]:
            self._length += 1
        self._hash_table[index] = (key, value, hash(key))

    def __resize(self) -> None:
        cells = [cell for cell in self._hash_table if cell]
        self._capacity *= 2
        self._hash_table = [None] * self._capacity
        self._length = 0
        for cell in cells:
            self[cell[0]] = cell[1]

    def __getitem__(self, key: Hashable) -> Any:
        index = self.__index(key)
        if self._hash_table[index]:
            return self._hash_table[index][1]
        raise KeyError

    def __index(self, key: Hashable) -> int:
        index = hash(key) % self._capacity
        while self._hash_table[index] and self._hash_table[index][0] != key:
            index = (index + 1) % self._capacity
        return index

    def clear(self) -> None:
        self._hash_table = [None] * self._capacity
        self._length = 0

    def __delitem__(self, key: Hashable) -> None:
        index = self.__index(key)
        if self._hash_table[index]:
            self._hash_table[index] = None
            self._length -= 1

    def get(self, key: Hashable, value: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return value

    def pop(self, key: Hashable, value: Any = None) -> Any:
        try:
            item = self[key]
            del self[key]
            return item
        except KeyError:
            if not value:
                raise
            return value

    def __iter__(self) -> iter:
        for cell in self._hash_table:
            if cell:
                yield cell[0]

    def items(self) -> tuple:
        for cell in self._hash_table:
            if cell:
                yield cell[:2]

    def values(self) -> Any:
        for cell in self._hash_table:
            if cell:
                yield cell[1]

    def __str__(self) -> str:
        return str([cell for cell in self.items()])

    def update(self, dict_: Dictionary) -> None:
        for key, value in dict_.items():
            self[key] = value
