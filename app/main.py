from typing import Any, Hashable


class Dictionary:
    def __init__(self, initial_capacity: int = 8) -> None:
        self.capacity = initial_capacity
        self.size = 0
        self.storage = [None] * self.capacity

    class Node:
        def __init__(self, key: Hashable, value: Any) -> None:
            self.key = key
            self.value = value
            self.next = None

    def __setitem__(self, key: Hashable, value: Any) -> None:
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

    def __getitem__(self, key: Hashable) -> Any:
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
