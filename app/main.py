from __future__ import annotations
from typing import Hashable, Iterator, Any


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.table = [[] for _ in range(self.capacity)]
        self.increase_factor = 0.66
        self.size = 0

    def __setitem__(self, key: Hashable, value: Any) -> None:
        hash_idx = self.get_indexes(key)
        for idx, (element, _) in enumerate(self.table[hash_idx]):
            if element == key:
                self.table[hash_idx][idx] = (key, value)
                return

        if self.size >= self.capacity * self.increase_factor:
            self.__resize()
            hash_idx = hash(key) % self.capacity

        self.table[hash_idx].append((key, value))
        self.size += 1

    def __getitem__(self, key: Hashable) -> Any:
        hash_idx = self.get_indexes(key)
        for element, value in self.table[hash_idx]:
            if element == key:
                return value
        raise KeyError

    def get(self, key: Hashable) -> Any:
        hash_idx = self.get_indexes(key)
        for element, value in self.table[hash_idx]:
            if element == key:
                return value
        return None

    def pop(self, key: Hashable) -> Any:
        value = self.get(key)
        if value is not None:
            self.__delitem__(key)
        return value

    def __iter__(self) -> Iterator[Hashable]:
        for element in self.table:
            for key, _ in element:
                yield key

    def __delitem__(self, key: Hashable) -> None:
        hash_idx = self.get_indexes(key)
        for idx, (element, value) in enumerate(self.table[hash_idx]):
            if element == key:
                del self.table[hash_idx][idx]
                self.size -= 1
                return
        raise KeyError

    def clear(self) -> None:
        self.__init__()

    def __resize(self) -> None:
        old_table = self.table[:]
        self.capacity *= 2
        self.table = [[] for _ in range(self.capacity)]
        self.size = 0

        for chunk in old_table:
            for key, value in chunk:
                self[key] = value

    def __len__(self) -> int:
        return self.size

    def get_indexes(self, key: Hashable) -> int:
        return hash(key) % self.capacity
