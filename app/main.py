from typing import Any, Hashable


class Dictionary:
    def __init__(self, capacity: int = 8, load_factor: float = 0.67) -> None:
        self.capacity = capacity
        self.load_factor = load_factor
        self.size = 0
        self.table = [None] * self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self._get_index(key)
        if self.table[index] is None:
            self.size += 1
        self.table[index] = (key, value)
        if self.size > self.capacity * self.load_factor:
            self._resize()

    def __getitem__(self, key: Hashable) -> Any:
        index = self._get_index(key)
        if self.table[index] is None:
            raise KeyError
        return self.table[index][1]

    def _get_index(self, key: Hashable) -> int:
        index = hash(key) % self.capacity
        while self.table[index] and self.table[index][0] != key:
            index = (index + 1) % self.capacity
        return index

    def __len__(self) -> int:
        return self.size

    def _resize(self) -> None:
        old_table = self.table
        self.capacity *= 2
        self.size = 0
        self.table = [None] * self.capacity
        for item in old_table:
            if item:
                self[item[0]] = item[1]
