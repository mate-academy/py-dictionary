from typing import Any


class Node:
    def __init__(self, key: Any, value: Any, key_hash: Any) -> None:
        self.key = key
        self.value = value
        self.hash = key_hash


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.size = 0
        self.data = [None] * self.capacity
        self.load_factor = 0.6

    def _index(self, key_hash: int) -> int:
        return key_hash % self.capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        key_hash = hash(key)
        index = self._index(key_hash)
        node = self.data[index]

        while node and node.key != key:
            index = (index + 1) % self.capacity
            node = self.data[index]

        if node is None:
            self.data[index] = Node(key, value, key_hash)
            self.size += 1
        else:
            node.value = value

        if self.size / self.capacity > self.load_factor:
            self._resize()

    def __getitem__(self, key: Any) -> Any:
        key_hash = hash(key)
        index = self._index(key_hash)

        node = self.data[index]
        while node and node.key != key:
            index = (index + 1) % self.capacity
            node = self.data[index]

        if node:
            return node.value
        raise KeyError(f"Key '{key}' not found")

    def __len__(self) -> int:
        return self.size

    def _resize(self) -> None:
        old_data = self.data
        self.capacity *= 2
        self.data = [None] * self.capacity
        self.size = 0

        for node in old_data:
            if node:
                self[node.key] = node.value
