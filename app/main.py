from __future__ import annotations

from dataclasses import dataclass
from typing import Any

Deleted = object()
_sentinel = object()


@dataclass
class Node:
    key_hash: int
    key: Any
    value: Any


class Dictionary:
    def __init__(self) -> None:
        self.capacity: int = 8
        self.length: int = 0
        self.load_factor_threshold: float = 0.66
        self.threshold: int = int(self.capacity * self.load_factor_threshold)
        self.hash_table: list[Any] = [None] * self.capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.length >= self.threshold:
            self._resize()

        key_hash = hash(key)
        index = key_hash % self.capacity
        first_deleted_index = None

        while True:
            node = self.hash_table[index]

            if node is None:
                new_node = Node(
                    key_hash=key_hash,
                    key=key,
                    value=value
                )
                if first_deleted_index is not None:
                    self.hash_table[first_deleted_index] = new_node
                else:
                    self.hash_table[index] = new_node

                self.length += 1
                break

            if node is Deleted:
                if first_deleted_index is None:
                    first_deleted_index = index
                index = (index + 1) % self.capacity
                continue

            if node.key == key:
                node.value = value
                break

            if node.key != key:
                index = (index + 1) % self.capacity

    def _resize(self) -> None:
        old_table = self.hash_table

        if self.length >= self.threshold:
            self.capacity *= 2

        self.threshold = int(self.capacity * self.load_factor_threshold)
        self.hash_table = [None] * self.capacity
        self.length = 0

        for node in old_table:
            if node is not None and node is not Deleted:
                self.__setitem__(node.key, node.value)

    def __getitem__(self, key: Any) -> None:
        key_hash = hash(key)
        index = key_hash % self.capacity

        while True:
            node = self.hash_table[index]
            if node is None:
                raise KeyError(key)

            if node is Deleted:
                index = (index + 1) % self.capacity
                continue

            if node.key == key:
                return node.value
            index = (index + 1) % self.capacity

    def __len__(self) -> int:
        return self.length

    def clear(self) -> None:
        self.length = 0
        self.capacity = 8
        self.threshold = int(self.capacity * self.load_factor_threshold)
        self.hash_table = [None] * self.capacity

    def __delitem__(self, key: Any) -> None:
        key_hash = hash(key)
        index = key_hash % self.capacity

        while True:
            node = self.hash_table[index]
            if node is None:
                raise KeyError(key)

            if node is Deleted or node.key != key:
                index = (index + 1) % self.capacity
                continue

            if node.key == key:
                self.hash_table[index] = Deleted
                self.length -= 1
                break

    def get(self, key: Any, default: Any = None) -> Any:
        try:
            value = self[key]
        except KeyError:
            return default

        return value

    def pop(self, key: Any, default: Any = _sentinel) -> Any:
        try:
            value = self[key]
        except KeyError:
            if default is not _sentinel:
                return default
            raise
        del self[key]
        return value

    def __iter__(self) -> Any:
        for node in self.hash_table:
            if node is not None and node is not Deleted:
                yield node.key

    def update(self, other: dict = None, **kwargs) -> None:

        if other is not None:
            if hasattr(other, "items"):
                iterable = other.items()
            else:
                iterable = other
            for pair in iterable:
                try:
                    k, v = pair
                except Exception:
                    raise TypeError("update() argument must be a "
                                    "mapping or iterable of pairs")
                self[k] = v

        if kwargs:
            for key, value in kwargs.items():
                self[key] = value
