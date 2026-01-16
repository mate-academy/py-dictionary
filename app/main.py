from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.capacity = 8
        self.load_factor = int(self.capacity * 2 / 3)
        self.hash_table: list = [None] * self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.length >= self.load_factor:
            self.resize()

        hash_key = hash(key)
        index = hash_key % self.capacity
        while True:
            if self.hash_table[index] is None:
                self.hash_table[index] = [hash_key, key, value]
                self.length += 1
                break
            if (self.hash_table[index][0] == hash_key
                    and self.hash_table[index][1] == key):
                self.hash_table[index][2] = value
                break
            index = (index + 1) % self.capacity

    def __getitem__(self, key: Hashable) -> Any:
        hash_key = hash(key)
        index = hash_key % self.capacity
        while self.hash_table[index] is not None:
            if (self.hash_table[index][0] == hash_key
                    and self.hash_table[index][1] == key):
                return self.hash_table[index][2]
            index = (index + 1) % self.capacity
        raise KeyError(f"{self.hash_table[index]} is None")

    def __len__(self) -> int:
        return self.length

    def resize(self) -> None:
        self.capacity *= 2
        self.load_factor = int(self.capacity * 2 / 3)
        copy_table = self.hash_table
        self.hash_table = [None] * self.capacity
        self.length = 0
        for item in copy_table:
            if item:
                self.__setitem__(item[1], item[2])

    def clear(self) -> None:
        self.hash_table = [None] * self.capacity
