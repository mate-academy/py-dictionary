from __future__ import annotations

from typing import Any, Hashable, Iterable


class Dictionary:
    def __init__(self, capacity: int = 8, load_factor: float = 2 / 3) -> None:
        self.capacity = capacity
        self.load_factor = load_factor
        self.size = 0
        self.table = [None] * self.capacity

    def _resize(self) -> None:
        table_copy = self.table[:]
        self.size = 0
        self.capacity *= 2
        self.table = [None] * self.capacity
        for node in table_copy:
            if node:
                self.__setitem__(node[0], node[2])

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.size > self.capacity * self.load_factor:
            self._resize()
        hashed_key = hash(key)
        index = hashed_key % self.capacity
        for index, node in enumerate(
                self.table[index:] + self.table[:index],
                start=index
        ):
            index %= self.capacity
            if node is None:
                self.table[index] = (key, hashed_key, value)
                self.size += 1
                return
            if (self.table[index][1] == hashed_key
                    and self.table[index][0] == key):
                self.table[index] = (self.table[index][0], hashed_key, value)
                return

    def __getitem__(self, key: Hashable) -> Any:
        index = hash(key) % self.capacity
        for node in self.table[index:] + self.table[:index]:
            if node is not None and node[1] == hash(key) and node[0] == key:
                return node[2]
        raise KeyError

    def __len__(self) -> int:
        return self.size

    def clear(self) -> None:
        self.__init__()

    def __delitem__(self, key: Hashable) -> None:
        index = hash(key) % self.capacity
        for index, node in enumerate(
                self.table[index:] + self.table[:index],
                start=index
        ):
            index %= self.capacity
            if node is not None and node[1] == hash(key) and node[0] == key:
                self.table[index] = None
                self.size -= 1
                return

    def get(self, key: Hashable, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: Hashable, default: Any = None) -> Any:
        try:
            value = self[key]
            del self[key]
            return value
        except KeyError:
            return default

    def update(self, other: Dictionary) -> None:
        for node in other.table:
            if node:
                self[node[0]] = node[2]

    def __iter__(self) -> Iterable:
        return map(lambda node: node[0],
                   filter(lambda node: node, self.table))
