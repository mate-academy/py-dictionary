from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.length = 0
        self.threshold = (self.capacity * 2 / 3) + 1
        self.hash_table = [None] * self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.threshold <= self.length:
            self.resize()
        index = hash(key) % self.capacity
        while True:
            if not self.hash_table[index]:
                self.hash_table[index] = [key, value]
                self.length += 1
                break
            if self.hash_table[index][0] == key:
                self.hash_table[index][1] = value
                break
            index = (index + 1) % self.capacity

    def __getitem__(self, key: Hashable) -> Any:
        index = hash(key) % self.capacity
        while True:
            if not self.hash_table[index]:
                raise KeyError
            if self.hash_table[index][0] == key:
                return self.hash_table[index][1]
            index = (index + 1) % self.capacity

    def __len__(self) -> None:
        return self.length

    def resize(self) -> None:
        old_hash_table = self.hash_table
        self.capacity *= 2
        self.threshold = (self.capacity * 2 / 3) + 1
        self.hash_table = [None] * self.capacity
        self.length = 0
        for index in old_hash_table:
            if index:
                self.__setitem__(index[0], index[1])
