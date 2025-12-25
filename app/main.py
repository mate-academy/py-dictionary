from typing import Hashable, Any


class Dictionary:
    def __init__(self,
                 capacity: int = 8,
                 load_factor: float = 2 / 3,
                 size: int = 0) -> None:
        self.load_factor = load_factor
        self.capacity = capacity
        self.size = size
        self.table = [None] * self.capacity

    def __getitem__(self, key: Hashable) -> Any:
        index = self.find_index(key)
        if self.table[index] is None:
            raise KeyError(f"Key '{key}' not found in the dictionary")
        return self.table[index][1]

    def __len__(self) -> int:
        return self.size

    def __delitem__(self, key: Hashable) -> None:
        index_key = self.hash_func(key)
        if self.table[index_key] and self.table[index_key][0] == key:
            del self.table[index_key]
            self.size -= 1

    def clear(self) -> None:
        self.capacity = 8
        self.table = []
        self.size = 0

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.size >= self.capacity * self.load_factor:
            self.resize()
        index = self.find_index(key)
        if self.table[index] is None:
            self.size += 1
        self.table[index] = [key, value, hash(key)]

    def hash_func(self, key: Hashable) -> int:
        return hash(key) % self.capacity

    def resize(self) -> None:
        old_table = self.table
        self.capacity *= 2
        self.table = [None] * self.capacity
        self.size = 0
        for item in old_table:
            if item is not None:
                self[item[0]] = item[1]

    def find_index(self, key: Hashable) -> int:
        index_key = self.hash_func(key)
        while self.table[index_key] and self.table[index_key][0] != key:
            index_key += 1
            index_key %= self.capacity
        return index_key
