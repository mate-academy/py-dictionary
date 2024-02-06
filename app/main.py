from typing import Any, Hashable


class Dictionary:
    LOAD_FACTOR = 2 / 3

    def __init__(self) -> None:
        self.capacity = 8
        self.hash_table = [None] * self.capacity
        self.count = 0

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self.calculate_index(key)

        if not self.hash_table[index]:

            if self.count >= int(self.capacity * Dictionary.LOAD_FACTOR):
                self.resize()
                index = self.calculate_index(key)
            self.count += 1
        self.hash_table[index] = (key, hash(key), value)

    def __getitem__(self, key: Hashable) -> Any:
        index = self.calculate_index(key)

        if not self.hash_table[index]:
            raise KeyError

        return self.hash_table[index][2]

    def __len__(self) -> int:
        return self.count

    def resize(self) -> None:
        self.capacity *= 2
        old_hash_table = self.hash_table
        self.hash_table = [None] * self.capacity
        self.count = 0

        for item in old_hash_table:
            if item:
                self[item[0]] = item[2]

    def calculate_index(self, key: Hashable) -> int:
        index = hash(key) % self.capacity

        while self.hash_table[index] and self.hash_table[index][0] != key:
            index = (index + 1) % self.capacity

        return index
