from __future__ import annotations
from typing import Any, Iterator, Hashable, Iterable


class Dictionary:
    initial_capacity = 8
    load_factor = 2 / 3

    def __init__(self) -> None:
        self.length = 0
        self.hash_table = [None] * self.initial_capacity

    class Node:
        def __init__(self, key: Hashable, key_hash: int, value: Any) -> None:
            self.key = key
            self.key_hash = key_hash
            self.value = value

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.length == int(self.initial_capacity * self.load_factor):
            self._resize()

        index = hash(key) % self.initial_capacity

        while self.hash_table[index] is not None:
            if self.hash_table[index].key == key:
                self.hash_table[index].value = value
                return

            index = (index + 1) % self.initial_capacity
        else:
            self.hash_table[index] = self.Node(key, hash(key), value)
            self.length += 1

    def __getitem__(self, key: Hashable) -> Any:
        index = hash(key) % self.initial_capacity
        while self.hash_table[index] is not None:
            if self.hash_table[index].key == key:
                return self.hash_table[index].value

            index = (index + 1) % self.initial_capacity

        raise KeyError(f"Key '{key}' is not found in the dictionary.")

    def __len__(self) -> int:
        return self.length

    def __delitem__(self, key: Hashable) -> None:
        index = hash(key) % self.initial_capacity

        while self.hash_table[index] is not None:
            if self.hash_table[index].key == key:
                self.hash_table[index] = None
                self.length -= 1

                self._rehash()
                return

            index = (index + 1) % self.initial_capacity

        raise KeyError(f"Key '{key}' is not found in the dictionary.")

    def __iter__(self) -> Iterator:
        for node in self.hash_table:
            if node is not None:
                yield node.key, node.value

    def __str__(self) -> str:
        return (
            "{"
            + ", ".join(
                f"{node.key}: {node.value}" for node in self.hash_table if node
            )
            + "}"

        )

    def clear(self) -> None:
        self.hash_table = [None] * self.initial_capacity
        self.length = 0

    def get(self, key: Hashable, default_value: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default_value

    def pop(self, key: Hashable, default_value: Any = None) -> Any:
        try:
            item = self[key]
            del self[key]
            return item
        except KeyError:
            if default_value is None:
                raise KeyError(
                    f"Key '{key}' is not found in the dictionary"
                    + "and no default value was given."
                )

            return default_value

    def update(self, other: Dictionary | dict | Iterable) -> None:
        if isinstance(other, Dictionary):
            for node in other.hash_table:
                if node is not None:
                    self[node.key] = node.value
        elif isinstance(other, dict):
            for key, value in other.items():
                self[key] = value
        else:
            for key, value in other:
                self[key] = value

    def _resize(self) -> None:
        self.initial_capacity *= 2
        self._rehash()

    def _rehash(self) -> None:
        new_hash_table = [None] * self.initial_capacity

        for node in self.hash_table:
            if node is not None:
                new_index = node.key_hash % self.initial_capacity

                while new_hash_table[new_index] is not None:
                    new_index = (new_index + 1) % self.initial_capacity

                new_hash_table[new_index] = node

        self.hash_table = new_hash_table
