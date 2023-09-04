from copy import copy
from typing import Hashable, Any


class Dictionary:

    def __init__(self) -> None:
        self.capacity = 8
        self.threshold = int(self.capacity * 2 / 3)
        self.hash_table = [[] for _ in range(self.capacity)]
        self.size = 0

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.size == self.threshold:
            self.resize()

        hash_key = hash(key)
        index = hash_key % self.capacity

        while True:
            if not self.hash_table[index]:
                self.hash_table[index] = [key, value, hash_key]
                self.size += 1
                break

            if self.hash_table[index][0] == key:
                self.hash_table[index][1] = value
                break

            index = (index + 1) % self.capacity

    def __getitem__(self, item: Hashable) -> Any:
        index = hash(item) % self.capacity

        while self.hash_table[index]:
            if self.hash_table[index][0] == item:
                return self.hash_table[index][1]

            index = (index + 1) % self.capacity

        raise KeyError

    def __len__(self) -> int:
        return self.size

    def resize(self) -> None:
        self.capacity *= 2
        self.threshold = int(self.capacity * 2 / 3)
        old_hash_table = copy(self.hash_table)
        self.hash_table = [[] for _ in range(self.capacity)]
        self.size = 0

        for item in old_hash_table:
            if item:
                self.__setitem__(item[0], item[1])
