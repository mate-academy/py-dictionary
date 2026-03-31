from typing import Any


class Dictionary:
    def __init__(self,
                 initial_capacity: int = 8,
                 load_factor: float = 0.7) -> None:
        self.capacity = initial_capacity
        self.load_factor = load_factor
        self.size = 0
        self.table = [None] * self.capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.size >= (self.capacity * self.load_factor):
            self.resize()
        index = hash(key) % self.capacity
        while self.table[index] is not None and self.table[index][0] != key:
            index = (index + 1) % self.capacity
        if self.table[index] is None:
            self.size += 1
        self.table[index] = (key, value)

    def resize(self) -> None:
        new_capacity = self.capacity * 2
        new_table = [None] * new_capacity
        for item in self.table:
            if item is not None:
                index = hash(item[0]) % new_capacity
                while new_table[index] is not None:
                    index = (index + 1) % new_capacity
                new_table[index] = item
        self.table = new_table
        self.capacity = new_capacity

    def __getitem__(self, key: Any) -> Any:
        index = hash(key) % self.capacity
        while self.table[index] is not None:
            if self.table[index][0] == key:
                return self.table[index][1]
            index = (index + 1) % self.capacity
        raise KeyError(f"Key {key} not found")

    def __len__(self) -> int:
        return self.size
