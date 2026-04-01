from copy import deepcopy
from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.length = 0
        self.hash_table: list = [None] * self.capacity
        self.copy_hash_table = None

    def __setitem__(self, key: Any, value: Any) -> None:

        if self.length >= round(self.capacity * (2 / 3)):
            self.capacity *= 2
            self.copy_hash_table = deepcopy(self.hash_table)
            self.hash_table: list = [None] * self.capacity
            self.length = 0

            for cell in self.copy_hash_table:
                if cell:
                    self.hash_distribution(cell[0], cell[2])
            self.copy_hash_table = None

        self.hash_distribution(key, value)

    def hash_distribution(self, key: Any, value: Any) -> None:
        index = hash(key) % self.capacity
        start_index = index

        while True:

            if self.hash_table[start_index] is None:
                self.hash_table[start_index] = [key, hash(key), value]
                break

            if self.hash_table[start_index][0] == key:
                self.hash_table[start_index] = [key, hash(key), value]
                self.length -= 1
                break

            start_index = (start_index + 1) % self.capacity

        self.length += 1

    def __getitem__(self, key: Any) -> Any:

        index = hash(key) % self.capacity
        start_index = index

        while True:
            required_key = self.hash_table[start_index]

            if required_key is None:
                raise KeyError

            if required_key[0] == key:
                return required_key[2]

            start_index = (start_index + 1) % self.capacity

    def __len__(self) -> int:
        return self.length
