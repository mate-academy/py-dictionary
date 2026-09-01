from dataclasses import dataclass
from typing import Any


@dataclass
class Node:
    key: Any
    hash_value: int
    value: Any


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.hash_table = [None] * 8

    def __len__(self) -> int:
        return self.length

    def __setitem__(self, key: Any, value: Any) -> None:
        hash_val = hash(key)
        index = hash_val % len(self.hash_table)
        while self.hash_table[index] is not None:
            node = self.hash_table[index]
            if node.key == key:
                node.value = value
                return
            index = (index + 1) % len(self.hash_table)
        self._resize_if_needed()
        index = hash_val % len(self.hash_table)
        while self.hash_table[index] is not None:
            index = (index + 1) % len(self.hash_table)
        self.hash_table[index] = Node(key, hash_val, value)
        self.length += 1

    def __getitem__(self, key: Any) -> Any:
        hash_val = hash(key)
        index = self._find_index(key, hash_val)
        node = self.hash_table[index]
        if node is not None:
            return node.value
        raise KeyError(f"Key {key} not found")

    def _resize(self) -> None:
        old_table = self.hash_table
        new_size = len(self.hash_table) * 2
        self.hash_table = [None] * new_size
        for node in old_table:
            if node is None:
                continue
            index = node.hash_value % len(self.hash_table)
            while self.hash_table[index] is not None:
                index = (index + 1) % len(self.hash_table)
            self.hash_table[index] = node

    def _load_factor(self) -> float:
        return self.length / len(self.hash_table)

    def _resize_if_needed(self) -> None:
        if self._load_factor() >= 0.75:
            self._resize()

    def _find_index(self, key: Any, hash_val: int) -> int:
        index = hash_val % len(self.hash_table)
        while (
            self.hash_table[index] is not None
            and self.hash_table[index].key != key
        ):
            index = (index + 1) % len(self.hash_table)
        return index

    def clear(self) -> None:
        self.hash_table = [None] * len(self.hash_table)
        self.length = 0

    def get(self, key: Any, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def update(self, other: dict) -> None:
        for key, value in other.items():
            self[key] = value

    def __iter__(self) -> Any:
        for node in self.hash_table:
            if node is not None:
                yield node.key
