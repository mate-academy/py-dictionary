from typing import Any, Hashable


class Dictionary:

    def __init__(self) -> None:
        self.capacity = 8
        self.threshold = int(self.capacity * 2 / 3)
        self.hash_table = [[] for _ in range(self.capacity)]
        self.storage = 0

    def __getitem__(self, key: Hashable) -> list:
        key_hash = hash(key)
        index = key_hash % self.capacity
        while True:
            try:
                if self.hash_table[index][1] == key:
                    return self.hash_table[index][2]
            except IndexError:
                raise KeyError
            index = (index + 1) % self.capacity

    def __len__(self) -> int:
        return self.storage

    def __setitem__(
            self,
            key: Hashable,
            value: Any
    ) -> None:
        if self.storage == self.threshold:
            self.resize()
        key_hash = (hash(key))
        index = key_hash % self.capacity
        while True:
            if not self.hash_table[index]:
                self.hash_table[index] = [key_hash, key, value]
                self.storage += 1
                break
            if self.hash_table[index][1] == key:
                self.hash_table[index][2] = value
                break
            index = (index + 1) % self.capacity

    def resize(self) -> None:
        hash_table_ = self.hash_table
        self.storage = 0
        self.capacity *= 2
        self.threshold = int(self.capacity * 2 / 3)
        self.hash_table = [[] for _ in range(self.capacity)]
        for item in hash_table_:
            if item:
                self.__setitem__(item[1], item[2])
