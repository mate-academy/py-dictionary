from typing import Any
from collections.abc import Hashable


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.capacity = 8
        self.hash_table = [None] * self.capacity

    def _resize(self) -> None:
        old_table = self.hash_table
        self.capacity *= 2
        self.hash_table = [None] * self.capacity
        self.length = 0

        for bucket in old_table:
            if bucket:
                for key, key_hash, value in bucket:
                    index = key_hash % self.capacity
                    if self.hash_table[index] is None:
                        self.hash_table[index] = [(key, key_hash, value)]
                    else:
                        self.hash_table[index].append((key, key_hash, value))
                    self.length += 1

    def __setitem__(self, key: Hashable, value: int) -> None:
        if self.length / self.capacity > 0.75:
            self._resize()

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
            raise KeyError(f"Key not found: {key}")
        else:
            for i, indie in enumerate(self.hash_table[index]):
                if indie[0] == key:
                    return indie[2]
            raise KeyError(f"Key not found: {key}")

    def __len__(self) -> int:
        return self.length
