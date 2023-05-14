from __future__ import annotations
from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.hash_table = [None] * self.capacity
        self.size = 0
        self.load_factor = 2 / 3

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.size > self.capacity * self.load_factor:
            self._resize()

        hash_key = hash(key)
        index = hash_key % self.capacity

        while self.hash_table[index] is not None:
            if self.hash_table[index][0] == key:
                self.hash_table[index] = (key, hash_key, value)
                return
            index = (index + 1) % self.capacity

        self.hash_table[index] = (key, hash_key, value)
        self.size += 1

    def __getitem__(self, key: Hashable) -> Any:
        return self.hash_table[self._get_item_index(key)][2]

    def __len__(self) -> int:
        return self.size

    def __delitem__(self, key: Hashable) -> None:
        self.hash_table[self._get_item_index(key)] = None

    def __iter__(self) -> Dictionary:
        self.index = -1
        return self

    def __next__(self) -> Any:
        while self.index < self.capacity and \
                self.hash_table[self.index] is not None:
            self.index += 1

        if self.index >= self.capacity:
            raise StopIteration

        return self.hash_table[self.index][0]

    def clear(self) -> None:
        self.capacity = [None] * self.capacity
        self.size = 0

    def get(self, key: Hashable) -> Any:
        try:
            return self[key]
        except KeyError:
            return None

    def pop(self, key: Hashable) -> Any:
        value = self[key]
        self.__delitem__(key)
        return value

    def update(self, items: Any) -> None:
        for item in items:
            self[item[0]] = item[1]

    def _resize(self) -> None:
        self.capacity *= 2
        new_hash_table = [None] * self.capacity

        for item in self.hash_table:
            if item is not None:
                index = item[1] % self.capacity
                while new_hash_table[index] is not None:
                    index = (index + 1) % self.capacity
                new_hash_table[index] = item
        self.hash_table = new_hash_table

    def _get_item_index(self, key: Hashable) -> int:
        hash_key = hash(key)
        index = hash_key % self.capacity

        while self.hash_table[index] is not None:
            if self.hash_table[index][0] == key:
                return index

            index = (index + 1) % self.capacity

        raise KeyError(key)
