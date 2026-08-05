from typing import Any


class Node:
    def __init__(self, key: Any, _hash: int, value: Any) -> None:
        self.key = key
        self.hash = _hash
        self.value = value


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.table = [None] * self.capacity
        self.length = 0

    def __setitem__(self, key: Any, value: Any) -> None:
        _hash = hash(key)
        index = _hash % self.capacity

        while self.table[index] is not None:
            node = self.table[index]

            if node.hash == _hash and node.key == key:
                node.value = value
                return
            index = (index + 1) % self.capacity

        self.table[index] = Node(key, _hash, value)
        self.length += 1
        if self.length / self.capacity >= 0.7:
            self._resize()

    def __getitem__(self, key: Any) -> object:
        _hash = hash(key)
        index = _hash % self.capacity

        while self.table[index] is not None:
            node = self.table[index]

            if node.hash == _hash and node.key == key:
                return node.value
            index = (index + 1) % self.capacity
        raise KeyError(f"Key '{key}' not found")

    def __len__(self) -> int:
        return self.length

    def _resize(self) -> None:
        old_table = self.table
        self.capacity *= 2
        self.table = [None] * self.capacity
        for node in old_table:
            if node is not None:
                index = node.hash % self.capacity
                while self.table[index] is not None:
                    index = (index + 1) % self.capacity
                self.table[index] = node
