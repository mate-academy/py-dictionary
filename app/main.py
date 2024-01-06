from typing import Hashable, Any


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.threshold = int(self.capacity * 2 / 3)
        self.length = 0
        self.hash_table = [[] for _ in range(self.capacity)]

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.length == self.threshold:
            self.resize()
        hash_key = hash(key)
        position = hash_key % self.capacity

        while True:
            if not self.hash_table[position]:
                self.hash_table[position] = [key, value, hash_key]
                self.length += 1
                return
            if self.hash_table[position][0] == key and\
                    self.hash_table[position][2] == hash_key:
                self.hash_table[position][1] = value
                return
            position = (position + 1) % self.capacity

    def __getitem__(self, key: Any) -> Any:
        position = hash(key) % self.capacity
        while True:
            if not self.hash_table[position]:
                raise KeyError(key)
            if self.hash_table[position][0] == key:
                return self.hash_table[position][1]
            position = (position + 1) % self.capacity

    def resize(self) -> None:
        old_table = self.hash_table
        self.capacity *= 2
        self.threshold = int(self.capacity * 2 / 3)
        self.length = 0
        self.hash_table = [[] for _ in range(self.capacity)]
        for item in old_table:
            if item:
                self.__setitem__(item[0], item[1])

    def __len__(self) -> int:
        return self.length
