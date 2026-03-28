from __future__ import annotations
from typing import Any, Iterator, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.hash_table: list = [None] * 8
        self.size = 8
        self.threshold = 0.66
        self.limit = round(self.size * self.threshold)
        self.keys = []

    def navigator(self, key: Hashable) -> int:
        hashed_key = hash(key)
        index = hashed_key % self.size
        while (self.hash_table[index] is not None
               and self.hash_table[index][0] != key):
            index = (index + 1) % self.size
        return index

    def resize(self) -> None:
        old_table = self.hash_table.copy()
        self.size *= 2
        self.hash_table: list = [None] * self.size
        self.length = 0
        self.limit = round(self.size * self.threshold)
        self.keys = []
        for node in old_table:
            if node is not None:
                self.__setitem__(node[0], node[1])

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.length >= self.limit:
            self.resize()
        index = self.navigator(key)
        if self.hash_table[index] is None:
            self.keys.append(key)
            self.length += 1
        self.hash_table[index] = (key, value)

    def __getitem__(self, key: Hashable) -> Any:
        index = self.navigator(key)
        if self.hash_table[index] is not None:
            return self.hash_table[index][1]
        raise KeyError

    def __delitem__(self, key: Hashable) -> None:
        index = self.navigator(key)
        if self.hash_table[index] is None:
            raise KeyError
        self.hash_table[index] = None
        self.keys.remove(key)
        self.length -= 1

    def __len__(self) -> int:
        return self.length

    def clear(self) -> None:
        self.hash_table: list = [None] * 8
        self.length = 0

    def get(self, key: Hashable, default: Any = None) -> Any:
        if key in self.keys:
            index = self.navigator(key)
            return self.hash_table[index][1]
        else:
            return default

    def pop(self, key: Hashable, default: Any = None) -> Any:
        if key in self.keys:
            value = self.__getitem__(key)
            self.__delitem__(key)
            return value
        elif default is not None:
            return default
        else:
            raise KeyError

    def __iter__(self) -> Iterator:
        result = []
        for node in self.hash_table:
            if node is not None:
                result.append(node[0])
        return iter(result)

    def update(self, iterable: dict | list | Dictionary) -> None:
        if isinstance(iterable, dict):
            for key, value in iterable.items():
                self.__setitem__(key, value)
        elif isinstance(iterable, list):
            for node in iterable:
                self.__setitem__(node[0], node[1])
        elif isinstance(iterable, Dictionary):
            for node in iterable.hash_table:
                if node is not None:
                    self.__setitem__(node[0], node[1])
        else:
            raise TypeError
