from __future__ import annotations
from typing import Any, List


class _Node:
    __slots__ = ("key", "hash", "value")

    def __init__(self, key: Any, h: int, value: Any) -> None:
        self.key = key
        self.hash = h
        self.value = value


class Dictionary:
    def __init__(self, initial_capacity: int = 8,
                 load_factor: float = 0.75) -> None:
        if initial_capacity <= 0:
            initial_capacity = 8
        self._capacity = initial_capacity
        self._buckets: List[List[_Node]] = [
            [] for _ in range(self._capacity)
        ]
        self._size = 0
        self._load_factor = load_factor

    def __len__(self) -> int:
        return self._size

    def _bucket_index(self, h: int) -> int:
        return h % self._capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        h = hash(key)
        index = self._bucket_index(h)
        bucket = self._buckets[index]

        for node in bucket:
            if node.hash == h and node.key == key:
                node.value = value
                return

        bucket.append(_Node(key, h, value))
        self._size += 1

        if self._size / self._capacity > self._load_factor:
            self._resize(self._capacity * 2)

    def __getitem__(self, key: Any) -> Any:
        h = hash(key)
        index = self._bucket_index(h)
        bucket = self._buckets[index]

        for node in bucket:
            if node.hash == h and node.key == key:
                return node.value

        raise KeyError(f"Key not found: {key!r}")

    def _resize(self, new_capacity: int) -> None:
        old_buckets = self._buckets
        self._capacity = new_capacity
        self._buckets = [[] for _ in range(self._capacity)]

        old_size = self._size
        self._size = 0

        for bucket in old_buckets:
            for node in bucket:
                index = self._bucket_index(node.hash)
                self._buckets[index].append(
                    _Node(node.key, node.hash, node.value)
                )
                self._size += 1

        assert self._size == old_size

    def __contains__(self, key: Any) -> bool:
        try:
            self[key]
            return True
        except KeyError:
            return False

    def __repr__(self) -> str:
        items = []
        for bucket in self._buckets:
            for node in bucket:
                items.append(f"{node.key!r}: {node.value!r}")
        return "{" + ", ".join(items) + "}"


class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __hash__(self) -> int:
        return hash(self.x) ^ (hash(self.y) << 1)

    def __eq__(self, other: Any) -> bool:
        return (
            isinstance(other, Point)
            and self.x == other.x
            and self.y == other.y
        )

    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y})"
