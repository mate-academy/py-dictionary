from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.table = [[] for _ in range(8)]
        self.capacity = 8
        self.size = 0
        self.load_factor = 2 / 3

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = hash(key) % self.capacity
        while self.table[index] and self.table[index][0] != key:
            index = (index + 1) % self.capacity

        if self.table[index] and self.table[index][0] == key:
            self.table[index][1] = value
        else:
            self.table[index] = [key, value]
            self.size += 1
        if self.size > self.load_factor * self.capacity:
            self.resize()

    def __getitem__(self, key: Hashable) -> Any:
        index = hash(key) % self.capacity
        while self.table[index] and self.table[index][0] != key:
            index = (index + 1) % self.capacity
        if self.table[index] and self.table[index][0] == key:
            return self.table[index][1]
        raise KeyError("Key not found")

    def __len__(self) -> int:
        return self.size

    def resize(self) -> None:
        old_table = self.table
        self.capacity *= 2
        self.size = 0
        self.table = [[] for _ in range(self.capacity)]
        for bucket in old_table:
            if bucket:
                self.__setitem__(bucket[0], bucket[1])
