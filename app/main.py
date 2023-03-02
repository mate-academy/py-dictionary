from typing import Any, Hashable


class Dictionary:
    def __init__(self,
                 capacity: int = 8,
                 load_factor: float = 0.75) -> None:
        self._capacity = capacity
        self._load_factor = load_factor
        self._size = 0
        self._table = [None] * capacity

    def __len__(self) -> int:
        return self._size

    def __getitem__(self, key: Hashable) -> None:
        index = self._find_index(key)
        if index == -1:
            raise KeyError(key)
        return self._table[index][2]

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self._find_index(key)
        if index == -1:
            self._add_key_value(key, value)
        if index != -1:
            self._table[index] = (key, self._hash(key), value)
        if self._size / self._capacity >= self._load_factor:
            self._resize()

    def _add_key_value(self, key: Hashable, value: Any) -> None:
        index = self._hash(key) % self._capacity
        while self._table[index] is not None:
            index = (index + 1) % self._capacity
        self._table[index] = (key, self._hash(key), value)
        self._size += 1

    def _resize(self) -> None:
        old_table = self._table
        self._capacity *= 2
        self._table = [None] * self._capacity
        self._size = 0

        for index, value in enumerate(old_table):
            if old_table[index] is not None:
                self._add_key_value(old_table[index][0], old_table[index][2])

    def _find_index(self, key: Hashable) -> int:
        index = self._hash(key) % self._capacity
        while self._table[index] is not None and self._table[index][0] != key:
            index = (index + 1) % self._capacity
        if self._table[index] is not None:
            return index
        return -1

    @staticmethod
    def _hash(key: Hashable) -> int:
        return hash(key)
