from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.length = 0
        self.hash_table = [None] * self.capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.length >= self.capacity * 2 / 3:
            self._resize()

        index = hash(key) % self.capacity

        while self.hash_table[index] is not None:
            existing_key, existing_hash, _ = self.hash_table[index]
            if existing_hash == hash(key) and existing_key == key:
                self.hash_table[index] = [key, hash(key), value]
                return
            index = (index + 1) % self.capacity

        self.hash_table[index] = [key, hash(key), value]
        self.length += 1

    def __getitem__(self, key: Any) -> None:
        index = hash(key) % self.capacity

        while self.hash_table[index] is not None:
            existing_key, existing_hash, value = self.hash_table[index]
            if existing_hash == hash(key) and existing_key == key:
                return value
            index = (index + 1) % self.capacity

        raise KeyError(key)

    def __len__(self) -> int:
        return self.length

    def _resize(self) -> None:
        old_table = self.hash_table
        self.capacity *= 2
        self.hash_table = [None] * self.capacity
        self.length = 0

        for node in old_table:
            if node is not None:
                key, _, value = node
                self[key] = value
