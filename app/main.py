from typing import Any


class Node:
    def __init__(self, key: Any, value: Any, key_hash: int) -> None:
        self.key = key
        self.value = value
        self.hash = key_hash


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.threshold = int(self.capacity * (2 / 3))
        self.table = [None] * self.capacity
        self.size = 0

    def _hash(self, key: Any) -> int:
        return hash(key) % self.capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.size > self.threshold:
            self._resize()

        index = self._hash(key)
        node = self.table[index]
        while node is not None and node.key != key:
            index = (index + 1) % len(self.table)
            node = self.table[index]
        if node is not None and node.key == key:
            node.value = value
            return
        self.table[index] = Node(key, value, key_hash=self._hash(key))
        self.size += 1

    def __getitem__(self, key: Any) -> Any:
        index = self._hash(key)
        node = self.table[index]
        while node is not None and node.key != key:
            index = (index + 1) % len(self.table)
            node = self.table[index]
        if node is None:
            raise KeyError(key)
        return node.value

    def _resize(self) -> None:
        old_table = self.table
        self.capacity *= 2
        self.threshold = int(self.capacity * (2 / 3))
        self.table = [None] * self.capacity
        self.size = 0

        for node in old_table:
            if node is not None:
                new_index = hash(node.key) % self.capacity
                while self.table[new_index] is not None:
                    new_index = (new_index + 1) % self.capacity
                self.table[new_index] = node
                self.size += 1

    def __len__(self) -> int:
        return self.size
