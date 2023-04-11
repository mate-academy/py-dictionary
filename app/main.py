from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.storage = 0
        self.threshold = int(self.capacity * 2 / 3)
        self.hash_table = [[] for _ in range(self.capacity)]

    def __setitem__(
            self,
            key: int | float | str | tuple | bool,
            value: Any
    ) -> None:
        if self.storage == self.threshold:
            self.extend()
        _hash = hash(key)
        index = _hash % self.capacity

        while True:
            if not self.hash_table[index]:
                self.hash_table[index] = [_hash, key, value]
                self.storage += 1
                break
            if self.hash_table[index][1] == key:
                self.hash_table[index][2] = value
                break
            index = (index + 1) % self.capacity

    def extend(self) -> None:
        copy_hash_table = self.hash_table
        self.storage = 0
        self.capacity *= 2
        self.threshold = int(self.capacity * 2 / 3)
        self.hash_table = [[] for _ in range(self.capacity)]

        for item in copy_hash_table:
            if item:
                self.__setitem__(item[1], item[2])

    def __getitem__(self, key: str | int | float | tuple | bool) -> list:
        _hash = hash(key)
        index = _hash % self.capacity

        while self.hash_table[index]:
            if self.hash_table[index][:2] == [_hash, key]:
                return self.hash_table[index][2]
            index = (index + 1) % self.capacity
        raise KeyError

    def __len__(self) -> int:
        return self.storage
