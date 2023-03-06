from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.size = 0
        self.hash_table = [None] * self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.size > int(self.capacity * (2 / 3)):
            self.resize()
        hashed = hash(key)
        index = hashed % self.capacity
        while True:
            if not self.hash_table[index]:
                self.hash_table[index] = [key, value, hashed]
                self.size += 1
                break
            if (self.hash_table[index][0] == key
                    and self.hash_table[index][2] == hashed):
                self.hash_table[index][1] = value
                break
            index = (index + 1) % self.capacity

    def __getitem__(self, key: Hashable) -> Any:
        hashed = hash(key)
        index = hashed % self.capacity
        while self.hash_table[index]:
            if (self.hash_table[index][0] == key
                    and self.hash_table[index][2] == hashed):
                return self.hash_table[index][1]
            index = (index + 1) % self.capacity
        raise KeyError

    def __len__(self) -> int:
        return self.size

    def resize(self) -> None:
        self.size = 0
        self.capacity *= 2
        hashed_table = self.hash_table
        self.hash_table = [None] * self.capacity
        for item in hashed_table:
            if item:
                self.__setitem__(item[0], item[1])
