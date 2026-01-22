from typing import Hashable, Any


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.capacity = 8
        self.hash_table: list = [None] * self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        _hash = hash(key)
        index = _hash % self.capacity
        if not self.hash_table[index]:
            self.length += 1
            self.hash_table[index] = [[key, _hash, value]]
            return
        for pair in self.hash_table[index]:
            if pair[0] == key:
                pair[2] = value
                return
        self.hash_table[index].append([key, _hash, value])
        self.length += 1

    def __getitem__(self, key: Hashable) -> Any:
        index = hash(key) % self.capacity
        if not self.hash_table[index]:
            raise KeyError(f"Key not found: {key}")
        for pair in self.hash_table[index]:
            if pair[0] == key:
                return pair[2]
        raise KeyError(f"Key not found: {key}")

    def __len__(self) -> int:
        return self.length
