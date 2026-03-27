from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterator


_MISSING = object()


@dataclass
class Node:
    key: Any
    hash_value: int
    value: Any


class Dictionary:
    def __init__(self, capacity: int = 8) -> None:
        self._capacity = capacity
        self._size = 0
        self._buckets: list[list[Node]] = [[] for _ in range(self._capacity)]
        self._load_factor = 0.75

    def __len__(self) -> int:
        return self._size

    def __setitem__(self, key: Any, value: Any) -> None:
        hash_value = hash(key)
        index = self._get_index(hash_value)
        bucket = self._buckets[index]

        for node in bucket:
            if node.hash_value == hash_value and node.key == key:
                node.value = value
                return

        bucket.append(Node(key=key, hash_value=hash_value, value=value))
        self._size += 1

        if self._size / self._capacity > self._load_factor:
            self._resize()

    def __getitem__(self, key: Any) -> Any:
        hash_value = hash(key)
        index = self._get_index(hash_value)
        bucket = self._buckets[index]

        for node in bucket:
            if node.hash_value == hash_value and node.key == key:
                return node.value

        raise KeyError(key)

    def __delitem__(self, key: Any) -> None:
        hash_value = hash(key)
        index = self._get_index(hash_value)
        bucket = self._buckets[index]

        for i, node in enumerate(bucket):
            if node.hash_value == hash_value and node.key == key:
                del bucket[i]
                self._size -= 1
                return

        raise KeyError(key)

    def __iter__(self) -> Iterator[Any]:
        for bucket in self._buckets:
            for node in bucket:
                yield node.key

    def _get_index(self, hash_value: int) -> int:
        return hash_value % self._capacity

    def _resize(self) -> None:
        old_buckets = self._buckets
        self._capacity *= 2
        self._buckets = [[] for _ in range(self._capacity)]
        self._size = 0

        for bucket in old_buckets:
            for node in bucket:
                self[node.key] = node.value

    def clear(self) -> None:
        self._buckets = [[] for _ in range(self._capacity)]
        self._size = 0

    def get(self, key: Any, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: Any, default: Any = _MISSING) -> Any:
        hash_value = hash(key)
        index = self._get_index(hash_value)
        bucket = self._buckets[index]

        for i, node in enumerate(bucket):
            if node.hash_value == hash_value and node.key == key:
                value = node.value
                del bucket[i]
                self._size -= 1
                return value

        if default is not _MISSING:
            return default

        raise KeyError(key)

    def update(self, other: Any) -> None:
        for key, value in other:
            self[key] = value
