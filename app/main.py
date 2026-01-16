"""
Attributes ending with "_ordered_" are for iteration and presentation only.
Good luck)
"""

from __future__ import annotations
from typing import Any, Hashable


class Dictionary:
    def __init__(self, *args) -> None:
        self.length = 0
        self.capacity = 8
        self.hash_table = [None] * self.capacity
        self.keys_table = [None] * self.capacity
        self.keys_ordered = []
        self.values_ordered = []
        if args:
            self.items = [*args]
            if len(self.items) % 2 != 0:
                raise KeyError(f"Number of arguments must be "
                               f"even: {len(self.items)} is not")
            for i in range(1, len(self.items), 2):
                self.__setitem__(self.items[i - 1], self.items[i])

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if isinstance(key, list) or isinstance(key, dict):
            raise TypeError(f"Type of key {key} ({type(key)}) is unhashable")
        if self.length == self.capacity // 1.5:
            self.resize()
        index_ = hash(key) % self.capacity
        if not isinstance(self.hash_table[index_], type(None)):
            if key in self.keys_table:
                prev_value = self.hash_table[self.keys_table.index(key)]
                self.values_ordered[
                    self.values_ordered.index(prev_value)
                ] = value
                self.hash_table[self.keys_table.index(key)] = value

            elif key != self.keys_table[index_]:
                index_ = self.hash_table.index(None)
                self.hash_table[index_] = value
                self.keys_table[index_] = key
                self.length += 1
        else:
            self.hash_table[index_] = value
            self.keys_table[index_] = key
            self.length += 1
        if key not in self.keys_ordered:
            self.keys_ordered.append(key)
        if self.hash_table.count(value) > self.values_ordered.count(value):
            self.values_ordered.append(value)

    def resize(self) -> None:
        self.length = 0
        self.capacity *= 2
        keys_copy = [
            key for key in self.keys_table if not isinstance(key, type(None))
        ]
        values_copy = [
            value for value in self.hash_table
            if not isinstance(value, type(None))
        ]
        self.keys_table = [None] * self.capacity
        self.hash_table = [None] * self.capacity
        for i in range(len(keys_copy)):
            self.__setitem__(keys_copy[i], values_copy[i])

    def __getitem__(self, key: Hashable, indx: bool = False) -> Any:
        if key not in self.keys_table:
            raise KeyError(f"Key {key} is not found.")
        index_ = 0
        try:
            while True:
                if key == self.keys_table[index_]:
                    if indx:
                        return self.hash_table[index_], index_
                    return self.hash_table[index_]
                index_ += 1
        except IndexError:
            return None

    def __len__(self) -> int:
        return self.length

    def clear(self) -> None:
        self.length = 0
        self.hash_table = [None] * 8
        self.keys_table = [None] * 8

    def __delitem__(self, key: Hashable) -> None:
        value = self.__getitem__(key, True)
        if value[0]:
            del self.hash_table[value[1]]
            del self.keys_table[value[1]]
            return
        self.keys_table[value[1]] = None

    def get(self, key: Hashable, default: Any = None) -> Any:
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def pop(self, key: Hashable, default: Any = KeyError) -> Any:
        res = self.get(key, default)
        try:
            self.__delitem__(key)
        except KeyError:
            pass
        return res

    def update(self, other: dict | Dictionary) -> None:
        if isinstance(other, dict):
            for key, value in other.items():
                self.__setitem__(key, value)
            return
        for i in range(len(other.hash_table)):
            if other.keys_table[i]:
                self.__setitem__(other.keys_table[i], other.hash_table[i])

    def __iter__(self) -> Any:
        self.indx = 0
        return self

    def __next__(self) -> Any:
        indx = self.indx
        if indx >= self.length:
            raise StopIteration
        self.indx += 1
        return self.keys_ordered[indx]

    def values(self) -> list:
        return self.values_ordered

    def keys(self) -> list:
        return self.keys_ordered

    def items(self) -> list:
        return [
            (self.keys_ordered[i],
             self.values_ordered[i]) for i in range(self.length)
        ]
