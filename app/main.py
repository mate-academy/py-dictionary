from __future__ import annotations
from typing import Any, Hashable


class Dictionary:
    def __init__(self, threshold: float = 2 / 3) -> None:
        self.threshold = threshold
        self._table_size = 8
        self._size = 0
        self.hash_table = [[] for _ in range(self._table_size)]

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if len(self) >= self._table_size * self.threshold:
            self._resize()

        key_hash = hash(key)
        index = key_hash % self._table_size

        if self.hash_table[index]:
            while self.hash_table[index]:
                if self.hash_table[index][1] == key:
                    self.hash_table[index][2] = value
                    return
                if index == self._table_size - 1:
                    index = 0
                index += 1
        self.hash_table[index].extend([key_hash, key, value])
        self._size += 1

    def __getitem__(self, item: Hashable) -> Any:
        return self._get_item(item)[1]

    def __delitem__(self, key: Hashable) -> Any:
        index, key = self._get_item(key)
        self.hash_table[index] = []

    def __len__(self) -> int:
        return self._size

    def _get_item(self, item: Hashable) -> tuple:
        item_hash = hash(item)
        index = item_hash % len(self.hash_table)
        if self.hash_table[index]:
            while self.hash_table[index][1] != item:
                if index == len(self.hash_table) - 1:
                    index = 0
                index += 1
            return index, self.hash_table[index][2]
        raise KeyError(f"No such key '{item}' in a dictionary")

    def _resize(self) -> None:
        new_table = [[] for _ in range(len(self.hash_table) * 2)]
        self._table_size *= 2
        for element in self.hash_table:
            if element:
                key_hash, key, value = element
                index = key_hash % self._table_size
                if new_table[index]:
                    while new_table[index]:
                        if index == self._table_size - 1:
                            index = 0
                        index += 1
                new_table[index].extend([key_hash, key, value])
        self.hash_table = new_table

    def clear(self) -> None:
        self.hash_table = [[] for _ in range(self._table_size)]

    def get(self, item: Hashable, default_value: Any = None) -> Any:
        try:
            return self.__getitem__(item)
        except (KeyError, IndexError):
            return default_value

    def pop(self, item: Hashable) -> None:
        index, value = self._get_item(item)
        self.hash_table[index] = []
        return value

    def update(self, other: Dictionary) -> None:
        for element in other.hash_table:
            if element:
                key_hash, key, value = element
                self[key] = value
