from __future__ import annotations
from typing import Hashable, Any


class Dictionary:
    DEFAULT_OBJECT = object()

    def __init__(self) -> None:
        self.load_factor = 2 / 3
        self.capacity = 8
        self.length = 0
        self.hash_table: list = [None] * 8

    def get_index(self, key: Hashable) -> int:
        return hash(key) % self.capacity

    def __len__(self) -> int:
        return self.length

    def __resize(self) -> None:
        self.capacity *= 2
        old_hash_table = self.hash_table
        self.hash_table: list = [None] * self.capacity

        self.length = 0
        for element in old_hash_table:
            if element:
                self.__setitem__(element[0], element[2])

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.length > self.load_factor * self.capacity:
            self.__resize()
        index = self.get_index(key)

        while True:
            if not self.hash_table[index]:
                self.hash_table[index] = [key, hash(key), value]
                self.length += 1
                break

            if self.hash_table[index][0] == key:
                self.hash_table[index][2] = value
                break
            index = (index + 1) % self.capacity

    def find_element(self, key: Hashable) -> int:
        index = self.get_index(key)
        element = self.hash_table[index]

        step = 0
        while step < self.capacity:
            if element and element[0] == key:
                return index

            step += 1
            index = (index + 1) % self.capacity
            element = self.hash_table[index]

        raise KeyError(key)

    def __getitem__(self, key: Hashable) -> Any:
        element = self.hash_table[self.find_element(key)]
        return element[2]

    def __delitem__(self, key: Hashable) -> None:
        index = self.find_element(key)

        self.hash_table[index] = None
        self.length -= 1

    def clear(self) -> None:
        self.length = 0
        self.capacity = 8
        self.hash_table = [None] * 8

    def get(self, key: Hashable, value: Any = None) -> Any:
        try:
            return self.__getitem__(key)
        except KeyError:
            return value

    def pop(self, key: Hashable, default: Any = DEFAULT_OBJECT) -> Any:
        try:
            value = self.__getitem__(key)
            self.__delitem__(key)
            return value
        except KeyError:
            if default is not self.DEFAULT_OBJECT:
                return default
            raise

    def items(self) -> list[tuple]:
        return [
            (element[0], element[2])
            for element in self.hash_table
            if element
        ]

    def update(self, other: Dictionary | dict) -> None:
        for key, value in other.items():
            self.__setitem__(key, value)

    def __iter__(self) -> iter:
        for element in self.hash_table:
            if element:
                yield element[0]
