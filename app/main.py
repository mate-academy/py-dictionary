from typing import Hashable, Any


class Dictionary:
    LOAD_FACTOR = 2 / 3

    def __init__(self) -> None:
        self.size = 0
        self.capacity = 8
        self.hash_table = [None] * self.capacity

    def _resize(self) -> None:
        self.capacity *= 2
        self.size = 0
        old_table = self.hash_table
        self.hash_table = [None] * self.capacity
        for key, value in filter(None, old_table):
            self.__setitem__(key, value)

    def _get_index(self, key: Hashable) -> Any:
        index = hash(key) % self.capacity
        while True:
            if (self.hash_table[index] is None
                    or self.hash_table[index][0] == key):
                return index
            index = (index + 1) % self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self._get_index(key)
        if self.hash_table[index] is None:
            self.hash_table[index] = (key, value)
            self.size += 1
        elif self.hash_table[index][0] == key:
            self.hash_table[index] = (key, value)
        else:
            raise ValueError("Hash collision occurred")
        if self.size > self.capacity * self.LOAD_FACTOR:
            self._resize()

    def __getitem__(self, key: Hashable) -> Any:
        index = self._get_index(key)
        if self.hash_table[index] is None:
            raise KeyError(key)
        return self.hash_table[index][1]

    def __len__(self) -> int:
        return self.size

    def clear(self) -> None:
        self.capacity = 8
        self.size = 0
        self.hash_table = [None] * self.capacity

    def __delitem__(self, key: Hashable) -> None:
        index = self._get_index(key)
        if self.hash_table[index] is None:
            raise KeyError(f"Key not found: {key}")
        self.hash_table[index] = None
        self.size -= 1

    def get(self, key: Hashable, default: Any = None) -> object:
        if key in self:
            return self[key]
        else:
            return default

    def pop(self, key: Hashable, default: Any = None) -> object:
        if key in self:
            value = self[key]
            del self[key]
            return value
        else:
            raise KeyError(key)

    def update(self, other: dict) -> None:
        for key, value in other.items():
            self[key] = value

    def __iter__(self) -> iter:
        yield from (item[0] for item in self.hash_table if item is not None)
