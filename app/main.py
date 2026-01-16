from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self.capacity: int = 8
        self.fullness: float = 2 / 3
        self.hash_table = [None] * self.capacity
        self.length = 0

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.length >= self.capacity * self.fullness:
            self.resize()
        key_index = self.get_index(key)
        if not self.hash_table[key_index]:
            self.length += 1
        self.hash_table[key_index] = (key, hash(key), value)

    def __getitem__(self, item: Any) -> Any:
        item_index = self.get_index(item)
        if self.hash_table[item_index]:
            return self.hash_table[item_index][2]
        raise KeyError

    def get_index(self, key: Any) -> int:
        index = hash(key) % self.capacity
        while self.hash_table[index] and self.hash_table[index][0] != key:
            index = (index + 1) % self.capacity
        return index

    def resize(self) -> None:
        hash_table = self.hash_table
        self.capacity = self.capacity * 2
        self.hash_table: list = [None] * self.capacity
        self.length = 0
        for item in hash_table:
            if item:
                self.__setitem__(item[0], item[2])

    def __len__(self) -> int:
        return self.length

    def __str__(self) -> str:
        result = {item[0]: item[2] for item in self.hash_table if item}
        return f"{result}"

    def __delitem__(self, key: Any) -> None:
        key_index = self.get_index(key)
        if self.hash_table[key_index] is not None:
            self.hash_table[key_index] = None
            self.length -= 1

    def clear(self) -> None:
        self.hash_table = [None] * self.capacity
        self.length = 0
