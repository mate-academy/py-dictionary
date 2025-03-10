from __future__ import annotations
from typing import Any


class Node:
    def __init__(self, key: Any, value: Any) -> None:
        self.key = key
        self.value = value


class Dictionary:
    def __init__(self) -> None:
        self.initial_size = 8
        self.buckets = [None] * self.initial_size
        self.load_factor = 0.7
        self.size = 0
        self.order = []

    def _resize(self) -> None:
        new_initial_size = self.initial_size * 2
        new_buckets = [None] * new_initial_size
        old_buckets = self.buckets
        self.buckets = new_buckets
        self.initial_size = new_initial_size

        for old_node in old_buckets:
            if old_node is not None:
                index = hash(old_node.key) % self.initial_size

                while self.buckets[index] is not None:
                    index = (index + 1) % self.initial_size

                self.buckets[index] = Node(old_node.key, old_node.value)

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.size >= self.initial_size * self.load_factor:
            self._resize()

        index = hash(key) % self.initial_size

        while self.buckets[index] is not None:
            node = self.buckets[index]
            if node.key == key:
                node.value = value
                return
            index = (index + 1) % self.initial_size

        self.buckets[index] = Node(key, value)
        self.size += 1
        self.order.append(key)

    def __getitem__(self, key: Any) -> Any:
        index = hash(key) % self.initial_size

        while self.buckets[index] is not None:
            node = self.buckets[index]
            if node.key == key:
                return node.value
            index = (index + 1) % self.initial_size

        raise KeyError(f"Key '{key}' not found")

    def __len__(self) -> int:
        return self.size

    def items(self) -> list:
        return [(key, self[key]) for key in self.order]

    def __repr__(self) -> str:
        return str({key: self[key] for key in self.order})

    def clear(self) -> None:
        self.size = 0
        self.order = []
        self.initial_size = 8
        self.buckets = [None] * self.initial_size

    def __delitem__(self, key: Any) -> None:
        index = hash(key) % self.initial_size

        while self.buckets[index] is not None:
            node = self.buckets[index]

            if node.key == key:
                self.buckets[index] = None
                self.size -= 1
                self.order.remove(key)
                return

            index = (index + 1) % self.initial_size

        raise KeyError(f"Key '{key}' not found")

    def get(self, key: Any, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: Any, default: Any = None) -> Any:
        index = hash(key) % self.initial_size

        while self.buckets[index] is not None:
            node = self.buckets[index]
            if node.key == key:
                value = node.value
                self.buckets[index] = None
                self.order.remove(key)
                self.size -= 1
                return value
            index = (index + 1) % self.initial_size

        if default is not None:
            return default
        raise KeyError(f"Key '{key}' not found")

    def update(self, other: Dictionary | dict) -> None:
        for key, value in other.items():
            self[key] = value

    def __iter__(self) -> iter:
        return iter(self.order)
