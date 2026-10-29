from collections.abc import Hashable
from typing import Any


class Dictionary:

    def __init__(self, capacity: int = 8) -> None:
        self.length = 0
        self.capacity = capacity
        self.hash_table: list = [None] * self.capacity
        self.threshold = self.capacity * 2 // 3

    def _resize(self) -> None:
        self.capacity *= 2
        self.threshold = self.capacity * 2 // 3
        new_hash_table: list = [None] * self.capacity

        for entry in self.hash_table:
            if entry:
                index = entry[2] & (self.capacity - 1)
                while new_hash_table[index] is not None:
                    index = (index + 1) & (self.capacity - 1)
                new_hash_table[index] = entry

        self.hash_table = new_hash_table

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.length >= self.threshold:
            self._resize()

        key_hash = hash(key)
        index = key_hash & (self.capacity - 1)

        while self.hash_table[index] is not None:
            if (
                    key_hash == self.hash_table[index][2]
                    and key == self.hash_table[index][0]
            ):
                self.hash_table[index][1] = value
                return
            index = (index + 1) & (self.capacity - 1)

        self.hash_table[index] = [key, value, key_hash]
        self.length += 1

    def __getitem__(self, key: Hashable) -> Any:
        key_hash = hash(key)
        index = key_hash & (self.capacity - 1)

        while self.hash_table[index] is not None:
            if (
                    self.hash_table[index][2] == key_hash
                    and self.hash_table[index][0] == key
            ):
                return self.hash_table[index][1]

            index = (index + 1) & (self.capacity - 1)

        raise KeyError(f"Key {key} not found")

    def __len__(self) -> int:
        return self.length

    def clear(self) -> None:
        self.capacity = 8  # або ваш початковий дефолтний розмір
        self.hash_table = [None] * self.capacity
        self.length = 0
        self.threshold = self.capacity * 2 // 3

    def __delitem__(self, key: Hashable) -> None:
        key_hash = hash(key)
        index = key_hash & (self.capacity - 1)

        while self.hash_table[index] is not None:
            if (
                    self.hash_table[index][2] == key_hash
                    and self.hash_table[index][0] == key
            ):
                self.hash_table[index] = None
                self.length -= 1

                next_index = (index + 1) & (self.capacity - 1)
                while self.hash_table[next_index] is not None:
                    item = self.hash_table[next_index]
                    self.hash_table[next_index] = None
                    self.length -= 1
                    self.__setitem__(item[0], item[1])
                    next_index = (next_index + 1) & (self.capacity - 1)
                return

            index = (index + 1) & (self.capacity - 1)

        raise KeyError(f"Key {key} not found")
