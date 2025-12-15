from typing import Any


class Node:
    def __init__(self, key: Any, value: Any) -> None:
        self.key = key
        self.value = value
        self.hash = hash(key)


class Dictionary:
    def __init__(self, initial_capacity: int = 8,
                 load_factor: float = 0.75) -> None:
        self.capacity = initial_capacity
        self.load_factor = load_factor
        self.size = 0
        self.buckets = [[] for _ in range(self.capacity)]

    def _hash(self, key: Any) -> int:
        return hash(key) % self.capacity

    def _resize(self) -> None:
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0

        for bucket in old_buckets:
            for node in bucket:
                self[node.key] = node.value

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.size / self.capacity > self.load_factor:
            self._resize()

        index = self._hash(key)
        bucket = self.buckets[index]

        for node in bucket:
            if node.key == key:
                node.value = value
                return

        bucket.append(Node(key, value))
        self.size += 1

    def __getitem__(self, key: Any) -> None:
        index = self._hash(key)
        bucket = self.buckets[index]

        for node in bucket:
            if node.key == key:
                return node.value
        raise KeyError(key)

    def __len__(self) -> None:
        return self.size

    def __repr__(self) -> str:
        items = []
        for bucket in self.buckets:
            for node in bucket:
                items.append(f"{node.key!r}: {node.value!r}")
        return "{" + ", ".join(items) + "}"
