from typing import Any


class Node:
    def __init__(self, key: Any, value: Any) -> None:
        self.key = key
        self.hash: int = hash(key)
        self.value = value


class Dictionary:
    INITIAL_CAPACITY: int = 8
    LOAD_FACTOR: float = 2 / 3

    def __init__(self) -> None:
        self.capacity: int = self.INITIAL_CAPACITY
        self.length: int = 0
        self.hash_table: list = [None] * self.capacity

    def _resize(self) -> None:
        old_table: list = self.hash_table
        self.capacity *= 2
        self.hash_table = [None] * self.capacity
        self.length = 0
        for node in old_table:
            if node is not None:
                self[node.key] = node.value

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.length >= self.capacity * self.LOAD_FACTOR:
            self._resize()
        index: int = hash(key) % self.capacity
        while self.hash_table[index] is not None:
            if self.hash_table[index].key == key:
                self.hash_table[index].value = value
                return
            index = (index + 1) % self.capacity
        self.hash_table[index] = Node(key, value)
        self.length += 1

    def __getitem__(self, key: Any) -> Any:
        index: int = hash(key) % self.capacity
        while self.hash_table[index] is not None:
            if self.hash_table[index].key == key:
                return self.hash_table[index].value
            index = (index + 1) % self.capacity
        raise KeyError(key)

    def __len__(self) -> int:
        return self.length
