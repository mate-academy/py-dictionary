from typing import Any


class Dictionary:
    def __init__(self, capacity: int = 8, load_factor: float = 0.7) -> None:
        self.capacity = capacity
        self.load_factor = load_factor
        self.size = 0
        self.table = [None] * capacity

    def _hash(self, key: Any) -> int:
        return hash(key) % self.capacity

    def _resize(self) -> None:
        new_capacity = self.capacity * 2
        new_table = [None] * new_capacity

        for item in self.table:
            if item:
                key, value = item
                new_index = hash(key) % new_capacity
                while new_table[new_index] is not None:
                    new_index = (new_index + 1) % new_capacity
                new_table[new_index] = (key, value)

        self.table = new_table
        self.capacity = new_capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.size / self.capacity > self.load_factor:
            self._resize()

        index = self._hash(key)

        while self.table[index] is not None:
            k, v = self.table[index]
            if k == key:
                self.table[index] = (key, value)
                return
            index = (index + 1) % self.capacity

        self.table[index] = (key, value)
        self.size += 1

    def __getitem__(self, key: Any) -> Any:
        index = self._hash(key)

        while self.table[index] is not None:
            k, v = self.table[index]
            if k == key:
                return v
            index = (index + 1) % self.capacity

        raise KeyError(f"Key '{key}' not found.")

    def __len__(self) -> int:
        return self.size

    def clear(self) -> None:
        self.table = [None] * self.capacity
        self.size = 0

    def __delitem__(self, key: Any) -> None:
        index = self._hash(key)
        while self.table[index] is not None:
            k, v = self.table[index]
            if k == key:
                self.table[index] = None
                self.size -= 1
                return
            index = (index + 1) % self.capacity
        raise KeyError(f"Key '{key}' not found.")

    def get(self, key: Any, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: Any, default: Any = None) -> Any:
        try:
            value = self[key]
            self.__delitem__(key)
            return value
        except KeyError:
            return default

    def __iter__(self) -> Any:
        for item in self.table:
            if item is not None:
                yield item[0]
