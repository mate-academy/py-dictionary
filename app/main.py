from typing import Any, Hashable


class Dictionary:
    def __init__(self, capacity: int = 8, load_factor: float = 2 / 3) -> None:
        self._capacity = capacity
        self._load_factor = load_factor
        self._size = 0
        self._table = [None] * self._capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self._get_index(key)
        if not self._table[index]:
            self._size += 1
        self._table[index] = (key, value)
        if self._size > self._capacity * self._load_factor:
            self._resize()

    def __getitem__(self, key: Hashable) -> Any:
        index = self._get_index(key)
        if not self._table[index]:
            raise KeyError
        return self._table[index][1]

    def _get_index(self, key: Hashable) -> int:
        index = hash(key) % self._capacity

        while self._table[index] and self._table[index][0] != key:
            index = (index + 1) % self._capacity

        return index

    def __len__(self) -> int:
        return self._size

    def _resize(self) -> None:
        old_table = self._table
        self._capacity *= 2
        self._size = 0
        self._table = [None] * self._capacity
        for item in old_table:
            if item:
                self[item[0]] = item[1]

    def clear(self) -> None:
        self._capacity = 8
        self._size = 0
        self._table = [None] * self._capacity
