from typing import Any, Hashable


class Dictionary:
    def __init__(self, capacity: int = 8, load_factor: float = 0.75) -> None:
        self.capacity = capacity
        self.load_factor = load_factor
        self.length = 0
        self.hash_table = [None] * self.capacity

    def __len__(self) -> int:
        return self.length

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = hash(key) % self.capacity
        while self.hash_table[index] is not None:
            if self.hash_table[index][0] == key:
                self.hash_table[index] = (key, value)
                return
            index = (index + 1) % self.capacity

        self.hash_table[index] = (key, value)
        self.length += 1

        if self.length / self.capacity >= self.load_factor:
            self._table_capacity_resize()

    def __getitem__(self, key: Hashable) -> None:
        index = hash(key) % self.capacity
        while self.hash_table[index] is not None:
            if self.hash_table[index][0] == key:
                return self.hash_table[index][1]
            index = (index + 1) % self.capacity

        raise KeyError(key)

    def _table_capacity_resize(self) -> None:
        self.capacity *= 2
        new_table = [None] * self.capacity

        for item in self.hash_table:
            if item is not None:
                key, value = item
                index = hash(key) % self.capacity
                while new_table[index] is not None:
                    index = (index + 1) % self.capacity
                new_table[index] = (key, value)

        self.hash_table = new_table
