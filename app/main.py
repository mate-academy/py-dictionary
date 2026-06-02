from typing import Any


class Dictionary:
    initial_capacity = 8
    load_factor = 2 / 3

    def __init__(self) -> None:
        self.capacity = self.initial_capacity
        self.length = 0
        self.hash_table: list = [None] * self.capacity

    def _resize(self) -> None:
        old_table = self.hash_table
        self.capacity *= 2
        self.hash_table = [None] * self.capacity
        self.length = 0

        for item in old_table:
            if item is not None:
                self.__setitem__(item[0], item[2])

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.length >= self.capacity * self.load_factor:
            self._resize()

        hash_value = hash(key)
        index = hash_value % self.capacity

        while self.hash_table[index] is not None:
            if (self.hash_table[index][1] == hash_value
                    and self.hash_table[index][0] == key):
                self.hash_table[index] = (key, hash_value , value)
                return
            index = (index + 1) % self.capacity

        self.hash_table[index] = (key, hash_value , value)
        self.length += 1

    def __getitem__(self, key: Any) -> Any:
        hash_value = hash(key)
        index = hash_value % self.capacity

        while self.hash_table[index] is not None:
            if (self.hash_table[index][1] == hash_value
                    and self.hash_table[index][0] == key):
                return self.hash_table[index][2]
            index = (index + 1) % self.capacity

        raise KeyError(f"Key '{key}' not found in dictionary")

    def __len__(self) -> int:
        return self.length
