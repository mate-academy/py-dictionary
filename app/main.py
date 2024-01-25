from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.load_factor = 2 / 3
        self.hash_table = [None] * self.capacity
        self.length = 0

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self.get_index(key)

        if not self.hash_table[index]:
            self.length += 1

            if self.length >= int(self.capacity * self.load_factor):
                self.resize()
                index = self.get_index(key)

        self.hash_table[index] = (key, hash(key), value)

    def __getitem__(self, key: Hashable) -> Any:
        index = self.get_index(key)

        if not self.hash_table[index]:
            raise KeyError

        return self.hash_table[index][2]

    def __len__(self) -> int:
        return self.length

    def resize(self) -> None:
        self.capacity *= 2
        hash_table = self.hash_table
        self.hash_table = [None] * self.capacity

        for node in hash_table:
            if node:
                key, hash_, value = node
                self.hash_table[self.get_index(key)] = (key, hash_, value)

    def get_index(self, key: Hashable) -> int:
        index = hash(key) % self.capacity

        while (self.hash_table[index]
                and self.hash_table[index][0] != key):
            index = (index + 1) % self.capacity

        return index
