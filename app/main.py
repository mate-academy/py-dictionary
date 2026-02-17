from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.length = 0
        self.hash_table: list = [None] * self.capacity
        self.load_factor = 0.66

    def __setitem__(self, key: str, value: Any) -> None:
        index = hash(key) % self.capacity

        while self.hash_table[index] is not None:
            old_key, old_value = self.hash_table[index]

            if old_key == key:
                self.hash_table[index] = (key, value)
                return
            index = (index + 1) % self.capacity

        self.hash_table[index] = (key, value)
        self.length += 1

        if self.length / self.capacity >= self.load_factor:
            self.resize()

    def resize(self) -> None:
        old_hash_table = self.hash_table
        self.capacity *= 2
        self.hash_table = [None] * self.capacity
        self.length = 0

        for item in old_hash_table:
            if item is not None:
                key, value = item
                self.__setitem__(key, value)

    def __getitem__(self, key: str) -> Any:
        index = hash(key) % self.capacity
        start_index = index

        while True:

            if self.hash_table[index] is None:
                raise KeyError("Key not found")

            saved_key, saved_value = self.hash_table[index]
            if saved_key == key:
                return saved_value

            index = (index + 1) % self.capacity

            if index == start_index:
                raise KeyError("Key not found")

    def __len__(self) -> int:
        return self.length
