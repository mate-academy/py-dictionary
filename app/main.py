from typing import Any, Hashable


class Dictionary:

    def __init__(self) -> None:
        self.length = 0
        self.capacity = 8
        self.hash_table: list = [None] * self.capacity
        self.threshold = int(self.capacity * 2 / 3)

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.length == self.threshold:
            self.resize()
        key_hash = hash(key)
        index = key_hash % self.capacity
        while True:
            if self.hash_table[index] is None:
                self.hash_table[index] = [key, key_hash, value]
                self.length += 1
                return
            if self.hash_table[index][0] == key and (
                    self.hash_table[index][1] == key_hash
            ):
                self.hash_table[index][2] = value
                return
            index = (index + 1) % self.capacity

    def resize(self) -> None:
        self.capacity *= 2
        old_table = self.hash_table
        self.threshold = int(self.capacity * 2 / 3)
        self.hash_table = [None] * self.capacity
        self.length = 0
        for node in old_table:
            if node is not None:
                self.__setitem__(node[0], node[2])

    def __getitem__(self, key: Hashable) -> None:
        index = hash(key) % self.capacity
        while True:
            if self.hash_table[index] is None:
                raise KeyError(key)
            if self.hash_table[index][0] == key:
                return self.hash_table[index][2]
            index = (index + 1) % self.capacity

    def __len__(self) -> int:
        return self.length
