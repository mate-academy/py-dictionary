from typing import Any, Hashable


class Dictionary:
    def __init__(self, capacity: int = 8, load_factor: float = 2 / 3) -> None:
        self.capacity = capacity
        self.load_factor = load_factor
        self.size = 0
        self.table = [None] * capacity

    def __setitem__(self, key: Hashable, value: Any) -> Any:
        if self.size > self.capacity * self.load_factor:
            self._resize()
        index = self._hash(key)
        if self.table[index] is None:
            self.table[index] = []
        for entry in self.table[index]:
            if entry[0] == key:
                entry[1] = value
                return
        self.table[index].append([key, value])
        self.size += 1

    def __getitem__(self, key: Hashable) -> Any:
        index = self._hash(key)
        if self.table[index]:
            for entry in self.table[index]:
                if entry[0] == key:
                    return entry[1]
        raise KeyError(key)

    def __len__(self) -> int:
        return self.size

    def _hash(self, key: Hashable) -> int:
        return hash(key) % self.capacity

    def _resize(self) -> None:
        new_capacity = self.capacity * 2
        new_table = [None] * new_capacity
        for bucket in self.table:
            if bucket is not None:
                for key, value in bucket:
                    new_index = hash(key) % new_capacity
                    if new_table[new_index] is None:
                        new_table[new_index] = []
                    new_table[new_index].append([key, value])
        self.table = new_table
        self.capacity = new_capacity
