from typing import Any
from collections.abc import Hashable


class Dictionary:
    def __init__(
            self,
            initial_capacity: int = 8,
            load_factor: float = 0.66
    ) -> None:
        self.initial_capacity = initial_capacity
        self.load_factor = load_factor
        self.size = 0
        self.capacity = initial_capacity
        self.table = [None] * initial_capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self._get_index(key)
        if self.table[index] is None:
            self.table[index] = []
        for item in self.table[index]:
            if item[0] == key:
                item[2] = value
                return
        self.table[index].append([key, hash(key), value])
        self.size += 1
        if self.size >= self.capacity * self.load_factor:
            self._resize()

    def __getitem__(self, key: Hashable) -> Any:
        index = self._get_index(key)
        if self.table[index] is None:
            raise KeyError(key)
        for item in self.table[index]:
            if item[0] == key:
                return item[2]
        raise KeyError(key)

    def __len__(self) -> int:
        return self.size

    def __delitem__(self, key: Hashable) -> None:
        index = self._get_index(key)
        if self.table[index] is None:
            raise KeyError(key)
        for index, item in enumerate(self.table[index]):
            if item[0] == key:
                del self.table[index][index]
                self.size -= 1
                return
        raise KeyError(key)

    def __iter__(self) -> Any:
        for cell in self.table:
            if cell is not None:
                for item in cell:
                    yield item[0]

    def _get_index(self, key: Hashable) -> int:
        return hash(key) % self.capacity

    def _resize(self) -> None:
        self.capacity *= 2
        new_table = [None] * self.capacity
        for cell in self.table:
            if cell is not None:
                for key, hash_key, value in cell:
                    index = hash_key % self.capacity
                    if new_table[index] is None:
                        new_table[index] = []
                    new_table[index].append([key, hash_key, value])
        self.table = new_table

    def clear(self) -> None:
        self.table = [None] * self.initial_capacity
        self.size = 0

    def get(self, key: Hashable, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: Hashable, default: Any = None) -> Any:
        try:
            value: Any = self[key]
            del self[key]
            return value
        except KeyError:
            return default

    def update(self, other_dict: dict) -> None:
        for key, value in other_dict.items():
            self[key] = value
