from typing import Any, Hashable


class Dictionary:

    def __init__(self, capacity: int = 8, load_factor: float = 2 / 3) -> None:
        self.capacity = capacity
        self.load_factor = load_factor
        self.hash_table = [[] for _ in range(self.capacity)]
        self.size = 0

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.size >= self.capacity * self.load_factor:
            self.resize()
        index = hash(key) % self.capacity
        while self.hash_table[index]:
            key_cell, hash_cell, value_cell = self.hash_table[index]
            if key == key_cell:
                self.hash_table[index] = (key, hash(key), value)
                return
            index = (index + 1) % self.capacity
        self.hash_table[index] = (key, hash(key), value)
        self.size += 1

    def __getitem__(self, key: Hashable) -> Any:
        index = hash(key) % self.capacity
        while self.hash_table[index]:
            key_cell, hash_cell, value_cell = self.hash_table[index]
            if key == key_cell:
                return value_cell
            index = (index + 1) % self.capacity
        raise KeyError

    def resize(self) -> None:
        old_table = self.hash_table
        self.capacity *= 2
        self.hash_table = [[] for _ in range(self.capacity)]
        self.size = 0
        for cell in old_table:
            if cell:
                key_cell, hash_cell, value_cell = cell
                self.__setitem__(key_cell, value_cell)

    def __len__(self) -> int:
        return self.size

    def clear(self) -> None:
        self.hash_table = [[] for _ in range(self.capacity)]
        self.size = 0

    def __delitem__(self, key: Hashable) -> None:
        index = hash(key) % self.capacity
        while self.hash_table[index]:
            key_cell, hash_cell, value_cell = self.hash_table[index]
            if key == key_cell:
                self.hash_table[index] = []
                self.size -= 1
                return
            index = (index + 1) % self.capacity
        raise KeyError(key)

    def get(self, key: Hashable, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def update(self, other: Any) -> None:
        for key, value in other.items():
            self[key] = value

    def __iter__(self) -> Any:
        for index in range(self.capacity):
            if self.hash_table[index] is not None:
                for cell in self.hash_table[index]:
                    yield cell
