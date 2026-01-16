from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.load_factor = 2 / 3
        self.length = 0
        self.hash_table = [None] * self.capacity

    def __len__(self) -> int:
        return self.length

    def index(self, key: Hashable) -> int:
        return hash(key) % self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.length > self.capacity * self.load_factor:
            self.resize()
        hash_key = self.index(key)
        while self.hash_table[hash_key] is not None:
            if self.hash_table[hash_key][0] == key:
                self.hash_table[hash_key] = (key, hash(key), value)
                return
            hash_key = (hash_key + 1) % self.capacity

        self.hash_table[hash_key] = (key, hash(key), value)
        self.length += 1

    def __getitem__(self, key: Hashable) -> Any:
        hash_key = self.index(key)
        while self.hash_table[hash_key] is not None:
            if self.hash_table[hash_key][0] == key:
                return self.hash_table[hash_key][2]
            hash_key = (hash_key + 1) % self.capacity
        raise KeyError(key)

    def resize(self) -> None:
        old_table = self.hash_table
        self.capacity *= 2
        self.hash_table = [None] * self.capacity
        self.length = 0
        for items in old_table:
            if items is not None:
                self.__setitem__(items[0], items[2])
