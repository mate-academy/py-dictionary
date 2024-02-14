from typing import Hashable, Any


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.hash_table: list = [None] * 8
        self.capacity = 8

    def resize(self) -> None:
        self.capacity *= 2
        self.length = 0
        temp_table = [item for item in self.hash_table if item is not None]
        self.hash_table = [None] * self.capacity
        for item in temp_table:
            key, hash_key, value = item
            self.__setitem__(key, value)

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.length > self.capacity * 2 / 3:
            self.resize()
        hash_key = hash(key)
        index = hash_key % self.capacity
        node = [key, hash_key, value]
        while True:
            if self.hash_table[index] is None:
                self.hash_table[index] = node
                self.length += 1
                break
            if key == self.hash_table[index][0]:
                self.hash_table[index][2] = value
                break
            index = (index + 1) % self.capacity

    def __getitem__(self, key: Hashable) -> None:
        hash_key = hash(key)
        index = hash_key % self.capacity
        while True:
            if self.hash_table[index] is None:
                raise KeyError
            if (
                hash_key == self.hash_table[index][1]
                and key == self.hash_table[index][0]
            ):
                return self.hash_table[index][2]
            index = (index + 1) % self.capacity

    def __len__(self) -> int:
        return self.length
