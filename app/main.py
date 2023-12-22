from typing import Any


class Dictionary:
    def __init__(self, length: int = 0, capacity: int = 8) -> None:
        self.length = length
        self.capacity = capacity
        self.load_factor = int(self.capacity * 2 / 3)
        self.hash_table: list = [None] * self.capacity

    def resize(self) -> None:
        self.length = 0
        self.capacity *= 2
        self.load_factor = int(self.capacity * 2 / 3)
        prev_hash_table = self.hash_table
        self.hash_table: list = [None] * self.capacity
        for item in prev_hash_table:
            if item:
                self[item[0]] = item[2]

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.length > self.load_factor:
            self.resize()
        index = hash(key) % self.capacity
        while True:
            if not self.hash_table[index]:
                self.hash_table[index] = [key, hash(key), value]
                self.length += 1
                break
            if self.hash_table[index][0] == key:
                self.hash_table[index][2] = value
                break
            index = (index + 1) % self.capacity

    def __getitem__(self, key: Any) -> Any:
        index = hash(key) % self.capacity
        while self.hash_table[index]:
            if self.hash_table[index][0] == key:
                return self.hash_table[index][2]
            index = (index + 1) % self.capacity
        raise KeyError

    def __len__(self) -> int:
        return self.length
