from typing import Hashable, Any


class Node:
    def __init__(self, key: Hashable, value: Any) -> None:
        self.key = key
        self.value = value

    def __repr__(self) -> str:
        return f"{self.key}: {self.value}"


class Dictionary:
    NEW_LEVEL = 2 / 3

    def __init__(self) -> None:
        self.capacity = 8
        self.hash_table = [None] * self.capacity
        self.length = 0

    def resize(self) -> None:
        old_hash_table = self.hash_table
        self.capacity *= 2
        self.hash_table = [None] * self.capacity
        self.length = 0
        for node in old_hash_table:
            if node is not None:
                self[node.key] = node.value

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = hash(key) % self.capacity
        while self.hash_table[index] is not None:
            if self.hash_table[index].key == key:
                self.hash_table[index].value = value
                return
            index = (index + 1) % self.capacity
        self.hash_table[index] = Node(key, value)
        self.length += 1
        if self.length > self.NEW_LEVEL * self.capacity:
            self.resize()

    def __getitem__(self, key: Hashable) -> Any:
        index = hash(key) % self.capacity
        while self.hash_table[index] is not None:
            if self.hash_table[index].key == key:
                return self.hash_table[index].value
            index = (index + 1) % self.capacity
        raise KeyError(key)

    def __str__(self) -> str:
        return str(self.hash_table)

    def __len__(self) -> int:
        return self.length
