from typing import Any


class Dictionary:
    def __init__(self, initial_capacity: int = 8) -> None:
        self.capacity = initial_capacity
        self.size = 0
        self.storage = [None] * self.capacity

    class Node:
        def __init__(self, key: Any, value: Any) -> None:
            self.key = key
            self.value = value
            self.next = None

    def _resize(self) -> None:
        new_capacity = self.capacity * 2
        new_storage = [None] * new_capacity

        for i in range(self.capacity):
            node = self.storage[i]
            while node:
                new_index = hash(node.key) % new_capacity
                new_node = self.Node(node.key, node.value)
                new_node.next = new_storage[new_index]
                new_storage[new_index] = new_node
                node = node.next

        self.capacity = new_capacity
        self.storage = new_storage

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.size / self.capacity > 0.7:
            self._resize()

        index = hash(key) % self.capacity
        node = self.storage[index]

        while node:
            if node.key == key:
                node.value = value
                return
            node = node.next

        new_node = self.Node(key, value)
        new_node.next = self.storage[index]
        self.storage[index] = new_node
        self.size += 1

    def __getitem__(self, key: Any) -> Any:
        index = hash(key) % self.capacity
        node = self.storage[index]

        while node:
            if node.key == key:
                return node.value
            node = node.next

        raise KeyError(f"Key {key} not found.")

    def __len__(self) -> int:
        return self.size

    def __repr__(self) -> str:
        return f"Dictionary with {self.size} items."
