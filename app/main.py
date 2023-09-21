from __future__ import annotations
from typing import Hashable, Any


class Dictionary:
    def __init__(self, capacity: int = 8, load_factor: float = 0.67) -> None:
        self._capacity = capacity
        self._load_factor = load_factor
        self._len = 0
        self._table = [None] * self._capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self._len > self._capacity * self._load_factor:
            self._increase_table_size()

        index = self._find_index(key)
        if not self._table[index]:
            self._len += 1
        self._table[index] = [hash(key), key, value]

    def _increase_table_size(self) -> None:
        old_table = self._table
        self._capacity *= 2
        self._table = [None] * self._capacity
        self._len = 0

        for item in old_table:
            if item:
                self.__setitem__(item[1], item[2])

    def _find_index(self, key: Hashable) -> int:
        index = hash(key) % self._capacity
        while self._table[index] and self._table[index][1] != key:
            index += 1
            index %= self._capacity

        return index

    def __getitem__(self, key: Hashable) -> Any:
        index = self._find_index(key)
        if not self._table[index]:
            raise KeyError(f"Key {key} is not in dictionary")
        return self._table[index][2]

    def __len__(self) -> int:
        return self._len

    def get(self, key: Hashable) -> Any:
        return self.__getitem__(key)

    def clear(self) -> Dictionary:
        self.__init__()

    def __delitem__(self, key: Hashable) -> None:
        index = self._find_index(key)
        if self._table[index]:
            self._table[index] = [None]
            self._len -= 1
