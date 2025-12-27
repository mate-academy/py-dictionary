from typing import Hashable


class Dictionary:
    def __init__(self) -> None:
        self.load_factor = 0.5
        self.capacity = 8
        self.size = 0
        self.limit = self.capacity * self.load_factor
        self.hash_table = [[]] * self.capacity

    def __getitem__(self, key: Hashable) -> any:
        index = hash(key) % self.capacity
        while self.hash_table[index]:
            if (self.hash_table[index][0] == key
                    and self.hash_table[index][1] == hash(key)):
                return self.hash_table[index][2]
            index = (index + 1) % self.capacity
        raise KeyError(f"There is no key {key}")

    def __setitem__(self, key: Hashable, value: any) -> None:
        if self.size > self.limit:
            self.resize()
        index = hash(key) % self.capacity
        while True:
            if not self.hash_table[index]:
                self.hash_table[index] = [key, hash(key), value]
                self.size += 1
                break
            if (self.hash_table[index][0] == key
                    and self.hash_table[index][1] == hash(key)):
                self.hash_table[index][2] = value
                break
            index = (index + 1) % self.capacity

    def resize(self) -> None:
        hash_table = self.hash_table
        self.size = 0
        self.capacity *= 2
        self.limit = self.capacity * self.load_factor
        self.hash_table = [[]] * self.capacity
        for element in hash_table:
            if element:
                self.__setitem__(element[0], element[2])

    def __len__(self) -> int:
        return self.size
