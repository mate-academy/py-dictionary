from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.load_factor = 0.75
        self.size = 0
        self.table = [None] * self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = hash(key) % self.capacity
        while self.table[index] is not None and self.table[index][0] != key:
            index = (index + 1) % self.capacity
        if self.table[index] is None:
            self.size += 1
        self.table[index] = (key, value)
        if self.size >= self.capacity * self.load_factor:
            self._resize()

    def _resize(self) -> None:
        old_table = self.table
        self.capacity *= 2
        self.size = 0
        self.table = [None] * self.capacity
        for items in old_table:
            if items is not None:
                self[items[0]] = items[1]

    def __getitem__(self, key: Hashable) -> None:
        index = hash(key) % self.capacity
        while self.table[index] is not None:
            if self.table[index][0] == key:
                return self.table[index][1]
            index = (index + 1) % self.capacity
        raise KeyError(key)

    def __len__(self) -> int:
        return self.size
