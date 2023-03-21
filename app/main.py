from typing import Any, Hashable


class Dictionary:
    def __init__(self, capacity: int = 8, load_factor: float = 0.66) -> None:
        self.capacity = capacity
        self.load_factor = load_factor
        self.size = 0
        self.hash_table = [None] * self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = hash(key) % self.capacity
        while (self.hash_table[index] is not None
               and self.hash_table[index][0] != key):
            index = (index + 1) % self.capacity
        if (self.hash_table[index] is not None
                and self.hash_table[index][0] == key):
            self.hash_table[index][2] = value
        if self.hash_table[index] is None:
            self.size += 1
            self.hash_table[index] = [key, hash(key), value]
        if self.size >= self.capacity * self.load_factor:
            self.resize()

    def __getitem__(self, key: Hashable) -> Any:
        index = hash(key) % self.capacity
        while self.hash_table[index] is not None:
            if self.hash_table[index][0] == key:
                return self.hash_table[index][2]
            index = (index + 1) % self.capacity
        raise KeyError(f"{key} is not in the dictionary")

    def resize(self) -> None:
        temp_table = self.hash_table
        self.capacity = self.capacity * 2
        self.hash_table = [None] * self.capacity
        self.size = 0
        for node in temp_table:
            if node is not None:
                self[node[0]] = node[2]

    def __len__(self) -> int:
        return self.size
