from typing import Hashable, Any


class Dictionary:
    def __init__(
            self,
            capacity: int = 8,
            load_factor: float = 2 / 3,
            size: int = 0
    ) -> None:

        self.load_factor = load_factor
        self.capacity = capacity
        self.size = size
        self.table = [None] * self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:

        if self.size >= self.capacity * self.load_factor:
            self.resize()

        if self.table[self.count_index(key)] is None:
            self.size += 1

        self.table[self.count_index(key)] = [key, value, hash(key)]

    def __getitem__(self, key: Hashable) -> Any:
        if self.table[self.count_index(key)] is None:
            raise KeyError(key)

        return self.table[self.count_index(key)][1]

    def __len__(self) -> int:
        return self.size

    def clear(self) -> None:
        self.capacity = 8
        self.table = []
        self.size = 0

    def __delitem__(self, key: Hashable) -> None:
        if (self.table[self.hash_func(key)]
                and self.table[self.hash_func(key)][0] == key):

            del self.table[self.hash_func(key)]
            self.size -= 1

    def hash_func(self, key: Hashable) -> int:
        return hash(key) % self.capacity

    def resize(self) -> None:
        temp_table = self.table

        self.capacity *= 2
        self.table = [None] * self.capacity
        self.size = 0

        for item in temp_table:
            if item:
                self[item[0]] = item[1]

    def count_index(self, key: Hashable) -> int:
        index = self.hash_func(key)

        while self.table[index] and self.table[index][0] != key:
            index += 1
            index %= self.capacity

        return index
