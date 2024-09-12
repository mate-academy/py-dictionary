from typing import Hashable, Any


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.load_factor = 2 / 3
        self.capacity = 8
        self.hash_table = [None] * self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:

        if not isinstance(key, Hashable):
            raise TypeError("unhashable type")

        index = hash(key) % self.capacity
        while self.hash_table[index]:
            if self.hash_table[index][0] == key:
                self.hash_table[index] = (key, hash(key), value)
                return

            index = (index + 1) % self.capacity

        if self.length > self.capacity * self.load_factor:
            self.resize()
            self[key] = value
            return

        self.hash_table[index] = (key, hash(key), value)
        self.length += 1

    def __getitem__(self, key: Hashable) -> Any:
        index = hash(key) % self.capacity

        while self.hash_table[index] and self.hash_table[index][0] != key:
            index = (index + 1) % self.capacity

        if not self.hash_table[index]:
            raise KeyError(f"{key}")

        return self.hash_table[index][2]

    def __len__(self) -> int:
        return self.length

    def resize(self) -> None:
        self.capacity *= 2
        self.length = 0
        new_hash_table = self.hash_table
        self.hash_table = self.capacity * [None]
        for item in new_hash_table:
            if item:
                self[item[0]] = item[2]
