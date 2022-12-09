from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.size = 0
        self.capacity = 8
        self.threshold = int(self.capacity * (2 / 3))
        self.hash_table = [[]] * self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.size > self.threshold:
            self.resize()
        hash_key = hash(key)
        index = hash_key % self.capacity
        while True:
            if not self.hash_table[index]:
                self.hash_table[index] = [key, value, hash_key]
                self.size += 1
                break
            if self.hash_table[index][2] == hash_key and\
                    self.hash_table[index][0] == key:
                self.hash_table[index][1] = value
                break
            index = (index + 1) % self.capacity

    def resize(self) -> None:
        current_table = self.hash_table
        self.size = 0
        self.capacity *= 2
        self.threshold = int(self.capacity * (2 / 3))
        self.hash_table = [[]] * self.capacity
        for item in current_table:
            if item:
                self.__setitem__(item[0], item[1])

    def __getitem__(self, key: Hashable) -> list:
        index = hash(key) % self.capacity
        while True:
            if self.hash_table[index] and key == self.hash_table[index][0]:
                return self.hash_table[index][1]
            if not self.hash_table[index]:
                raise KeyError(f"There is no item named {key} in the dict")
            index = (index + 1) % self.capacity

    def __len__(self) -> int:
        return self.size
