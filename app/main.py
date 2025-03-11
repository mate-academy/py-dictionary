from typing import Any


class Node:
    def __init__(self, key: Any, value: Any) -> None:
        self.key = key
        self.value = value
        self.next = None


class Dictionary:
    def __init__(self, capacity: int = 8, load_factor: float = 2 / 3) -> None:
        self.capacity = capacity
        self.load_factor = load_factor
        self.size = 0
        self.nodes = [None] * self.capacity

    def _hash(self, key: Any) -> int:
        return hash(key) % self.capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        index = self._hash(key)
        node = self.nodes[index]

        if node is None:
            self.nodes[index] = Node(key, value)
            self.size += 1
        else:
            prev = None
            while node:
                if node.key == key:
                    node.value = value
                    return
                prev, node = node, node.next

            prev.next = Node(key, value)
            self.size += 1

        if self.size / self.capacity > self.load_factor:
            self._resize()

    def __getitem__(self, key: Any) -> None:
        index = self._hash(key)
        node = self.nodes[index]

        while node:
            if node.key == key:
                return node.value
            node = node.next

        raise KeyError(f"Key '{key}' not found")

    def __len__(self) -> int:
        return self.size

    def _resize(self) -> None:
        new_capacity = self.capacity * 2
        new_buckets = [None] * new_capacity
        old_buckets = self.nodes

        self.capacity = new_capacity
        self.nodes = new_buckets
        self.size = 0

        for node in old_buckets:
            while node:
                self[node.key] = node.value
                node = node.next
