from typing import Hashable, Any


class Dictionary:
    def __init__(self, capacity: int = 8, load_factor: float = 0.75) -> None:
        self.capacity = capacity
        self.load_factor = load_factor
        self.size = 0
        self.table = [None] * self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        table = self.table
        index = self._get_index(key)
        while table[index] is not None and table[index][0] != key:
            index = (index + 1) % self.capacity
        if table[index] is None:
            self.size += 1
        table[index] = (key, hash(key), value)
        if self.size > self.capacity * self.load_factor:
            self._resize()

    def __getitem__(self, key: Hashable) -> Any:
        index = self._get_index(key)
        if self.table[index] is None:
            raise KeyError(key)
        return self.table[index][2]

    def __len__(self) -> int:
        return self.size

    def _get_index(self, key: Hashable) -> int:
        index = hash(key) % self.capacity
        while self.table[index] is not None and self.table[index][0] != key:
            index = (index + 1) % self.capacity
        return index

    def _resize(self) -> None:
        self.capacity *= 2
        old_table = self.table
        self.table = [None] * self.capacity
        self.size = 0
        for item in old_table:
            if item is not None:
                key, hash_value, value = item
                self[key] = value

    def clear(self) -> None:
        self.capacity = 8
        self.size = 0
        self.table = [None] * self.capacity

    def __delitem__(self, key: Hashable) -> None:
        index = self._get_index(key)
        if self.table[index] is None:
            raise KeyError
        self.table[index] = None
        self.size -= 1

    def get(self, key: Hashable, default: Any = None) -> object:
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: Hashable, default: Any = None) -> object:
        try:
            value = self[key]
            del self[key]
            return value
        except KeyError:
            return default

    def update(self, other: dict) -> None:
        for key, value in other.items():
            self[key] = value

    def __iter__(self) -> iter:
        for item in self.table:
            if item is not None:
                yield item[0]
