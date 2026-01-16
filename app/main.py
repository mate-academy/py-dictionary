from typing import Any


class Node:
    def __init__(self, key: Any, hash_value: int, value: Any) -> None:
        self.key = key
        self.hash = hash_value
        self.value = value


class Dictionary:
    def __init__(
            self,
            initial_capacity: int = 8,
            load_factor: float = 0.66
    ) -> None:
        self.capacity = initial_capacity
        self.load_factor = load_factor
        self.size = 0
        self.table = [[] for _ in range(initial_capacity)]

    def hash_function(self, key: Any) -> int:
        return hash(key) % self.capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        hash_value = self.hash_function(key)
        node = Node(key, hash_value, value)
        bucket = self.table[hash_value]
        for item in bucket:
            if item.key == key:
                item.value = value
                return
        bucket.append(node)
        self.size += 1
        if self.size > self.capacity * self.load_factor:
            self.resize()

    def __getitem__(self, key: Any) -> Any:
        hash_value = self.hash_function(key)
        bucket = self.table[hash_value]
        for item in bucket:
            if item.key == key:
                return item.value
        raise KeyError

    def __len__(self) -> int:
        return self.size

    def resize(self) -> None:
        self.capacity *= 2
        new_table = [[] for _ in range(self.capacity)]
        for bucket in self.table:
            for node in bucket:
                new_hash_value = self.hash_function(node.key)
                new_table[new_hash_value].append(node)
        self.table = new_table
