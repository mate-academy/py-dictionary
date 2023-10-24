from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.length: int = 0
        self.capacity: int = 8
        self.load_factor: float = 2 / 3
        self.hash_table: list = [None] * self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        hash_key = hash(key)
        index = hash_key % self.capacity
        node = [key, hash_key, value]

        while True:
            if self.hash_table[index] is None:
                self.hash_table[index] = node
                self.length += 1
                break
            if self.hash_table[index][0] == key:
                self.hash_table[index][2] = value
                break
            index = (index + 1) % self.capacity

        if self.length >= self.capacity * self.load_factor:
            self.__resize()

    def __getitem__(self, key: Hashable) -> Any:
        index = hash(key) % self.capacity
        while self.hash_table[index] is not None:
            if self.hash_table[index][0] == key:
                return self.hash_table[index][2]
            index = (index + 1) % self.capacity
        raise KeyError(f"{key} is not in the dictionary")

    def __resize(self) -> None:
        self.capacity *= 2
        self.length = 0
        temp_table = self.hash_table
        self.hash_table = [None] * self.capacity
        for item in temp_table:
            if item:
                self.__setitem__(item[0], item[2])

    def __len__(self) -> int:
        return self.length
