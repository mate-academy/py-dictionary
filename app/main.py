from typing import Any, Hashable

LOAD_FACTOR = 2 / 3


class Node:
    def __init__(
            self,
            key: Hashable,
            hash_value: int,
            value: Any
    ) -> None:
        self.key = key
        self.hash_value = hash_value
        self.value = value


class Dictionary:
    def __init__(
            self,
            capacity: int = 8,
    ) -> None:
        self.capacity = capacity
        self.load_factor = LOAD_FACTOR
        self.size = 0
        self.hash_table = [[] for _ in range(self.capacity)]

    def __getitem__(
            self,
            key: Hashable
    ) -> Any:
        hash_value = self._get_hash(key)
        for bucket in self.hash_table[hash_value]:
            if bucket.key == key:
                return bucket.value
        raise KeyError

    def __len__(self) -> int:
        return self.size

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.size > self.capacity * self.load_factor:
            self._resize()
        hash_value = self._get_hash(key)
        for bucket in self.hash_table[hash_value]:
            if bucket.key == key and bucket.hash_value == hash_value:
                bucket.value = value
                return
        self.hash_table[hash_value].append(Node(key, hash_value, value))
        self.size += 1

    def _get_hash(self, key: Hashable) -> int:
        return hash(key) % self.capacity

    def _resize(self) -> None:
        new_size = self.capacity * 2
        new_hash_table = [[] for _ in range(new_size)]
        for cell in self.hash_table:
            for entry in cell:
                new_hash_value = hash(entry.key) % new_size
                new_hash_table[new_hash_value].append(entry)
        self.hash_table = new_hash_table
        self.capacity = new_size
