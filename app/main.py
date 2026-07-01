from typing import Any
from collections.abc import Hashable


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.capacity = 8
        self.hash_table = [None] * self.capacity

    def __setitem__(self, key: Hashable, value: int) -> None:
        index = hash(key) % self.capacity
        if self.hash_table[index] is None:
            self.hash_table[index] = [(key, hash(key), value)]
            self.length += 1
        else:
            for i, node in enumerate(self.hash_table[index]):
                if node[0] == key:
                    self.hash_table[index][i] = (key, hash(key), value)
                    return
            self.hash_table[index].append((key, hash(key), value))
            self.length += 1

    def __getitem__(self, key: Hashable) -> Any:
        index = hash(key) % self.capacity
        if self.hash_table[index] is None:
            raise KeyError(key)
        else:
            for i, indie in enumerate(self.hash_table[index]):
                if indie[0] == key:
                    return indie[2]
            raise KeyError(key)

    def __len__(self) -> int:
        return self.length
