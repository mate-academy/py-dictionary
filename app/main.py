from __future__ import annotations
from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self._load_factor = 2 / 3
        self._initial_capacity = 8
        self._nodes = [None] * self._initial_capacity

        self._size = 0
        self._index = 0

    def _resize(self) -> None:
        self._initial_capacity *= 2
        old_nodes = self._nodes.copy()
        old_size = self._size

        self._nodes = [None] * self._initial_capacity

        for node in old_nodes:
            if node is not None:
                key, hash_key, value = node
                self[key] = value
                self._size = old_size

    def __setitem__(self, key: Any, value: Any) -> None:
        self._size += 1

        if round(self._initial_capacity * self._load_factor) < self._size:
            self._resize()

        hash_key = hash(key)
        index = hash_key % self._initial_capacity

        while self._nodes[index] is not None:
            node_key = self._nodes[index][0]
            if node_key == key:
                self._size -= 1
                break
            index = index + 1 if index < self._initial_capacity - 1 else 0

        self._nodes[index] = (key, hash_key, value)

    def __getitem__(self, key: Any) -> None:
        hash_key = hash(key)
        index = hash_key % self._initial_capacity

        if self._nodes[index] is not None:
            node_key, node_hash_key, node_value = self._nodes[index]
            while node_key != key:
                index = index + 1 if index < self._initial_capacity - 1 else 0
                node_key, node_hash_key, node_value = self._nodes[index]

            return node_value
        else:
            raise KeyError("No such key in dictionary")

    def __len__(self) -> int:
        return self._size

    def clear(self) -> None:
        self._nodes = [None] * self._initial_capacity

    def __delitem__(self, key: Any) -> None:
        hash_key = hash(key)
        index = hash_key % self._initial_capacity

        self._nodes[index] = None

    def get(self, key: Any) -> Any:
        try:
            return self[key]
        except KeyError:
            return None

    def pop(self, key: Any) -> Any:
        value = self[key]
        del self[key]

        return value

    def __iter__(self) -> Dictionary:
        return self

    def __next__(self) -> Any:
        while self._index < self._initial_capacity:

            if self._nodes[self._index] is None:
                self._index += 1
                continue

            value = self._nodes[self._index]
            self._index += 1

            return value

        else:
            raise StopIteration("Dictionary index out of range")

    def keys(self) -> set[Any]:
        return {node[0] for node in self._nodes if node is not None}

    def update(self, other: Dictionary) -> None:
        for key in other.keys():
            self[key] = other[key]

    def __str__(self) -> str:
        return (
            f"{{{', '.join([f'{key}: {self[key]}' for key in self.keys()])}}}"
        )
