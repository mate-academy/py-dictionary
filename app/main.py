from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.load_factor = 2 / 3
        self.size = 0
        self.hash_table: list = [None] * 8

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.size >= self.capacity * self.load_factor:
            self.resize()

        index = self.count_index(key)
        if not self.hash_table[index]:
            self.size += 1

        self.hash_table[self.count_index(key)] = [key, value, hash(key)]

    def __getitem__(self, key: Hashable) -> Any:
        index = self.count_index(key)
        if not self.hash_table[index]:
            raise KeyError(key)
        return self.hash_table[index][1]

    def __len__(self) -> int:
        return self.size

    def resize(self) -> None:
        temp_table = self.hash_table
        self.capacity *= 2
        self.hash_table = [None] * self.capacity
        self.size = self.__len__()
        for item in temp_table:
            if item:
                key = item[0]
                self.hash_table[self.count_index(key)] = item

    def count_index(self, key: Hashable) -> int:
        index = hash(key) % self.capacity
        while self.hash_table[index] and self.hash_table[index][0] != key:
            index += 1
            index %= self.capacity
        return index

    def clear(self) -> None:
        self.hash_table = [None] * self.capacity
        self.size = 0

    def __delitem__(self, key: Hashable) -> None:
        index = hash(key) % self.capacity
        if not self.hash_table[index]:
            raise KeyError(key)
        self.hash_table[index] = None
        self.size -= 1
