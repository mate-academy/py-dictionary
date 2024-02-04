from typing import Any, Hashable


class Dictionary(object):

    def __init__(self) -> None:
        self._capacity = 8
        self._size = 0
        self._table = [None] * self._capacity

    def __getitem__(self, key: Hashable) -> Any:
        index = self.get_index(key, hash(key))

        if self._table[index] is None:
            raise KeyError(f"{key} is not found")

        return self._table[index][2]

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self._size * 3 > self._capacity * 2:
            self._resize()

        key_hash = hash(key)
        index = self.get_index(key, key_hash)
        if self._table[index] is None:
            self._size += 1

        self._table[index] = (key, key_hash, value)

    def __len__(self) -> int:
        return self._size

    def get_index(self, key: Hashable, key_hash: int) -> int:
        index = key_hash % self._capacity

        while self._table[index] is not None and self._table[index][0] != key:
            index += 1
            index %= self._capacity
        return index

    def _resize(self) -> None:
        table_copy = self._table
        self._capacity *= 2
        self._table = [None] * self._capacity
        self._size = 0
        for item in table_copy:
            if item is not None:
                self[item[0]] = item[2]
