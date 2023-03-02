from typing import Any, Hashable


CAPACITY = 8
LOAD_FACTOR = 2 / 3


class Dictionary:
    def __init__(self) -> None:
        self.size = 0
        self.capacity = CAPACITY
        self.hash_table = [None] * self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.size >= int(self.capacity * LOAD_FACTOR):
            self._resize()

        hashed_key, index = self.hash_key_and_index(key)

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
        hashed_key, index = self.hash_key_and_index(key)

        while self.hash_table[index]:
            if self.hash_table[index][0] == key:
                return self.hash_table[index][1]
            index = (index + 1) % self.capacity

        raise KeyError(f"{key} does`t exist")

    def __len__(self) -> int:
        return self.size

    def hash_key_and_index(self, key: Hashable) -> tuple:
        hashed_key = hash(key)
        index = hashed_key % self.capacity
        return hashed_key, index

    def _resize(self) -> None:
        self.capacity *= 2
        self.size = 0
        full_table = self.hash_table
        self.hash_table = [None] * self.capacity
        for item in full_table:
            if item:
                self[item[0]] = item[1]
