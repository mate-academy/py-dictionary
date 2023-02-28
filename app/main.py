from math import ceil
from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.size = 0
        self.capacity = 8
        self.hash_table = [None] * self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.size >= ceil(self.capacity * 2 / 3):
            self._resize()

        hashed_key = hash(key)
        index = hashed_key % self.capacity

        while True:
            if not self.hash_table[index]:
                self.hash_table[index] = [key, value, hashed_key]
                self.size += 1
                break
            elif (
                self.hash_table[index][0] == key
                and self.hash_table[index][2] == hashed_key
            ):
                self.hash_table[index][1] = value
                break
            else:
                index = (index + 1) % self.capacity

    def __getitem__(self, key: Hashable) -> Any:
        hashed_key = hash(key)
        index = hashed_key % self.capacity

        while self.hash_table[index]:
            if self.hash_table[index][0] == key:
                return self.hash_table[index][1]
            index = (index + 1) % self.capacity

        raise KeyError(f"{key} do not exist")

    def __len__(self) -> int:
        return self.size

    def _resize(self) -> None:
        self.capacity *= 2
        self.size = 0
        full_table = self.hash_table
        self.hash_table = [None] * self.capacity
        for item in full_table:
            if item:
                self[item[0]] = item[1]
