from copy import deepcopy
from typing import Hashable, Any


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.capacity = 8
        self.load_factor = 2 / 3
        self.table = [[] for _ in range(8)]

    def __setitem__(self, key: Hashable, value: Any) -> None:
        threshold = int(self.capacity * self.load_factor)
        if self.length == threshold:
            self.resize()

        hash_ = hash(key)
        index = hash_ % self.capacity

        while True:
            if not self.table[index]:
                self.table[index] = [key, value, hash_]
                self.length += 1
                return

            if self.table[index][2] == hash_ and self.table[index][0] == key:
                self.table[index][1] = value
                return
            index = (index + 1) % self.capacity

    def __getitem__(self, key: Hashable) -> list:
        hash_ = hash(key)
        index = hash_ % self.capacity

        while self.table[index]:
            if self.table[index][2] == hash_ and self.table[index][0] == key:
                return self.table[index][1]
            index = (index + 1) % self.capacity
        raise KeyError(key)

    def __len__(self) -> int:
        return self.length

    def resize(self) -> None:
        old_table = deepcopy(self.table)
        self.length = 0
        self.capacity *= 2
        self.table = [[] for _ in range(self.capacity)]
        for x in old_table:
            if x:
                self[x[0]] = x[1]
