from typing import Any, Hashable


class Dictionary:
    pass

    def __init__(self, capacity: int = 8, load_factor: float = 0.67) -> None:
        self.capacity = capacity
        self.load_factor = load_factor
        self.size = 0
        self.table = [None] * self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self._get_index(key)
        if self.table[index] is None:
            self.size += 1
            self.table[index] = (key, hash(key), value)
        elif self.table[index] is not None:
            self.table[index] = (key, hash(key), value)
        if self.size > self.capacity * self.load_factor:
            self._resize()

    def __getitem__(self, key: Hashable) -> Any:
        index = self._get_index(key)
        if self.table[index] is None:
            raise KeyError(key)
        return self.table[index][2]

    def __len__(self) -> int:
        return self.size

    def _get_index(self, key: Hashable) -> int:
        index = hash(key) % self.capacity
        while self.table[index] is not None and self.table[index][0] != key:
            index = (index + 1) % self.capacity
        return index

    def _resize(self) -> None:
        self.capacity *= 2
        old_table = self.table
        self.table = [None] * self.capacity
        self.size = 0
        for node in old_table:
            if node:
                self[node[0]] = node[2]
