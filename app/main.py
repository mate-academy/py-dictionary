from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.threshold = int(self.capacity * 2 / 3)
        self.table = [[] for _ in range(self.capacity)]
        self.storage = 0

    def __getitem__(self,
                    key: (int, float, str, tuple, bool)) -> None | list:
        key_hash = hash(key)
        hash_index = key_hash % self.capacity

        while True:
            try:
                if self.table[hash_index][0] == key\
                   and self.table[hash_index][1] == key_hash:
                    return self.table[hash_index][2]

            except IndexError:
                raise KeyError

            hash_index = (hash_index + 1) % self.capacity

    def __setitem__(self,
                    key: (int, float, str, tuple, bool),
                    value: Any) -> None:
        if self.storage == self.threshold:
            self.resize()

        key_hash = (hash(key))
        hash_index = key_hash % self.capacity
        while True:
            if not self.table[hash_index]:
                self.table[hash_index] = [key, key_hash, value]
                self.storage += 1
                break

            if self.table[hash_index][0] == key and\
                    self.table[hash_index][1] == key_hash:
                self.table[hash_index][2] = value
                break

            hash_index = (hash_index + 1) % self.capacity

    def __len__(self) -> int:
        return self.storage

    def resize(self) -> None:
        old_hash_table = self.table
        self.storage = 0
        self.capacity *= 2
        self.threshold = int(self.capacity * 2 / 3)
        self.table = [[] for _ in range(self.capacity)]

        for slot in old_hash_table:
            if slot:
                self.__setitem__(slot[0], slot[2])
