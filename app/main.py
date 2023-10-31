from typing import Hashable


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.size = 0
        self.load_factor = self.capacity * 2 / 3
        self.table = [None] * self.capacity

    def __setitem__(self, key: Hashable, value: int) -> None:
        if self.size > self.load_factor:
            self.resize()

        hash_key = hash(key)
        index = hash_key % self.capacity

        while True:
            if self.table[index] is None:
                self.table[index] = [key, hash_key, value]
                self.size += 1
                break
            if self.table[index][0] == key:
                self.table[index][2] = value
                break
            if index == self.capacity - 1:
                index = 0
            index += 1

    def __getitem__(self, key: Hashable) -> int:
        for item in self.table:
            if item:
                if item[0] == key and item[1] == hash(key):
                    return item[2]
        raise KeyError

    def resize(self) -> None:
        self.capacity *= 2
        self.load_factor = self.capacity * 2 / 3
        current_table = self.table
        self.table = [None] * self.capacity
        self.size = 0
        for item in current_table:
            if item:
                self[item[0]] = item[2]

    def __len__(self) -> int:
        return self.size
