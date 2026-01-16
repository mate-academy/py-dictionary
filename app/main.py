from typing import Any


class Dictionary:
    def __init__(self, capacity: int = 8, load_factor: float = 0.75) -> None:
        self.capacity = capacity
        self.load_factor = load_factor
        self.size = 0
        self.table = [None] * self.capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        index = hash(key) % self.capacity
        while True:
            if self.table[index] is None:
                self.table[index] = (key, value)
                self.size += 1
                break
            elif self.table[index][0] == key:
                self.table[index] = (key, value)
                break
            index = (index + 1) % self.capacity

        if self.size / self.capacity > self.load_factor:
            self._resize()

    def _resize(self) -> None:
        new_capacity = self.capacity * 2
        new_table = [None] * new_capacity

        for item in self.table:
            if item is not None:
                key, value = item
                index = hash(key) % new_capacity
                while new_table[index] is not None:
                    index = (index + 1) % new_capacity
                new_table[index] = (key, value)

        self.table = new_table
        self.capacity = new_capacity

    def __getitem__(self, key: Any) -> Any:
        index = hash(key) % self.capacity
        while self.table[index] is not None:
            stored_key, value = self.table[index]
            if stored_key == key:
                return value
            index = (index + 1) % self.capacity
        raise KeyError(f"Key {key} not found")

    def __len__(self) -> int:
        return self.size
