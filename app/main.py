from typing import Hashable, Any


class Dictionary:
    def __init__(self,
                 capacity: int = 8,
                 load_factor: float = 2 / 3) -> None:
        self.capacity = capacity
        self.load_factor = load_factor
        self.size = 0
        self.hash_table = [None] * self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self._get_index(key)
        if self.hash_table[index] is None:
            self.size += 1
            self.hash_table[index] = (key, hash(key), value)
        elif self.hash_table[index] is not None:
            self.hash_table[index] = (key, hash(key), value)
        if self.size > self.load_factor * self.capacity:
            self._resize()

    def __getitem__(self, key: Hashable) -> Any:
        index = self._get_index(key)
        if self.hash_table[index] is None:
            raise KeyError(key)
        return self.hash_table[index][2]

    def __len__(self) -> int:
        return self.size

    def _get_index(self, key: Hashable) -> int:
        index = hash(key) % self.capacity
        while (self.hash_table[index] is not None
               and self.hash_table[index][0] != key):
            index = (index + 1) % self.capacity
        return index

    def _resize(self) -> None:
        self.capacity *= 2
        previous_table = self.hash_table
        self.hash_table = [None] * self.capacity
        self.size = 0
        for node in previous_table:
            if node:
                self[node[0]] = node[2]
