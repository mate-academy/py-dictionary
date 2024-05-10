from typing import Hashable, Any


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.load_factor = 2 / 3
        self.size = 0
        self.table = [None] * self.capacity

    def _index(self, key: Hashable) -> int:
        return hash(key) % self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self._index(key)
        while self.table[index] is not None:
            if self.table[index][0] == key:
                self.table[index] = (key, value)
                return
            index = (index + 1) % self.capacity

        self.table[index] = (key, value)
        self.size += 1

        if self.size / self.capacity >= self.load_factor:
            self._resize()

    def __getitem__(self, key: Hashable) -> None:
        index = self._index(key)
        while self.table[index] is not None:
            if self.table[index][0] == key:
                return self.table[index][1]
            index = (index + 1) % self.capacity

        raise KeyError(key)

    def _resize(self) -> None:
        self.capacity *= 2
        new_table = [None] * self.capacity

        for item in self.table:
            if item is not None:
                key, value = item
                index = self._index(key)
                while new_table[index] is not None:
                    index = (index + 1) % self.capacity
                new_table[index] = (key, value)

        self.table = new_table

    def __len__(self) -> int:
        return self.size
