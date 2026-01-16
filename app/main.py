from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Hashable


@dataclass
class Node:
    key: Hashable
    value: Any


class Dictionary(object):

    def __init__(self, capacity: int = 8) -> None:
        self._capacity = capacity
        self._size = 0
        self._table: list[None | Node] = [None] * self._capacity

    def __getitem__(self, key: Hashable) -> Any:
        index = self.get_index(key)

        if not self._table[index]:
            raise KeyError(f"Key: {key} is not found!")

        return self._table[index].value

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self.get_index(key)
        if not self._table[index]:
            if self._size + 1 >= self._capacity * 2 / 3:
                self._resize()
                return self.__setitem__(key, value)

            self._size += 1
        self._table[index] = Node(key, value)

    def __delitem__(self, key: Hashable) -> None:
        index = self.get_index(key)

        if self._table[index] is None:
            raise KeyError(f"Key: {key} is not found!")

        self._table[index] = None
        self._size -= 1

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Any:
        for cell in self._table:
            if cell:
                yield cell.key

    def __str__(self) -> str:
        return str(self._table)

    def get_index(self, key: Hashable) -> int:
        index = hash(key) % self._capacity

        while (self._table[index]
               and self._table[index].key != key):
            index = (index + 1) % self._capacity

        return index

    def _resize(self) -> None:
        table_copy = self._table
        self.__init__(self._capacity * 2)
        for item in table_copy:
            if item:
                self.__setitem__(item.key, item.value)

    def clear(self) -> None:
        self._table = [None] * self._capacity
        self._size = 0

    def get(self, key: Hashable, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: Hashable, default: Any = None) -> Any:
        try:
            value: Any = self[key]
            del self[key]
            return value
        except KeyError:
            if default is None:
                raise KeyError
            return default

    def update(self, other_dict: dict | Dictionary) -> None:
        for key, value in other_dict.items():
            self[key] = value
