from typing import Hashable, Any


class Dictionary:
    def __init__(
            self, capacity: int = 10, load_factor: float = 0.7
    ) -> None:
        self.capacity = capacity
        self.load_factor = load_factor
        self.size = 0
        self.table = [None] * capacity

    @staticmethod
    def _hash(key: Hashable) -> int:
        return hash(key)

    def _resize(self) -> None:
        new_capacity = self.capacity * 2
        new_table = [None] * new_capacity
        for chain in self.table:
            current = chain
            while current:
                index = self._hash(current[0]) % new_capacity
                new_table[index] = [current[0], current[1], new_table[index]]
                current = current[2]
        self.table = new_table
        self.capacity = new_capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self._hash(key) % self.capacity
        current = self.table[index]
        while current:
            if current[0] == key:
                current[1] = value
                return
            current = current[2]
        self.table[index] = [key, value, self.table[index]]
        self.size += 1
        if self.size > self.capacity * self.load_factor:
            self._resize()

    def __getitem__(self, key: Hashable) -> Any:
        index = self._hash(key) % self.capacity
        current = self.table[index]
        while current:
            if current[0] == key:
                return current[1]
            current = current[2]
        raise KeyError(key)

    def __len__(self) -> int:
        return self.size
