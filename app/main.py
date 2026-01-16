from typing import Any


class Dictionary:
    def __init__(self, initial_capacity: int = 8) -> None:
        self.initial_capacity = initial_capacity
        self.table = [None] * initial_capacity
        self.size = 0

    def _resize_table(self) -> None:
        old_table = self.table
        self.initial_capacity *= 2
        self.table = [None] * self.initial_capacity
        self.size = 0
        for data in old_table:
            if data is not None:
                self.__setitem__(data[0], data[1])

    def __setitem__(self, key: Any, value: Any) -> None:
        _hash = hash(key)
        threshold = int(self.initial_capacity * (2 / 3))
        first_index = int(_hash % self.initial_capacity)
        for i in range(self.initial_capacity):
            second_index = (first_index + i) % self.initial_capacity
            if self.table[second_index] is None:
                self.table[second_index] = (key, value)
                self.size += 1
                if self.size > threshold:
                    self._resize_table()
                return
            if (
                    self.table[second_index] is not None
                    and self.table[second_index][0] == key
            ):
                self.table[second_index] = (key, value)
                return

    def __getitem__(self, key: Any) -> None:
        _hash = hash(key)
        first_index = int(_hash % self.initial_capacity)
        for i in range(self.initial_capacity):
            second_index = (first_index + i) % self.initial_capacity
            if self.table[second_index] is None:
                break
            if self.table[second_index][0] == key:
                return self.table[second_index][1]
        raise KeyError(f"Key '{key}' not found")

    def __len__(self) -> int:
        return self.size
