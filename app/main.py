from __future__ import annotations

from fractions import Fraction
from typing import Hashable, Any


class Dictionary:
    LOAD_FACTOR = Fraction(2, 3)

    class Node:
        def __init__(self, key: Hashable, value: Any) -> None:
            self.key = key
            self.value = value

    def __init__(self) -> None:
        self.capacity = 8
        self.size = 0
        self.hash_table: list[Dictionary.Node | None] = [None] * self.capacity

    def _resize(self) -> None:
        old_hash_table = self.hash_table

        self.capacity *= 2
        self.size = 0
        self.hash_table: list[Dictionary.Node | None] = [None] * self.capacity

        for node in old_hash_table:
            if node:
                self[node.key] = node.value

    def _calculate_index(self, key: Hashable) -> int:
        index = hash(key) % self.capacity

        while (
            self.hash_table[index] is not None
            and self.hash_table[index].key != key
        ):
            index = (index + 1) % self.capacity

        return index

    def __setitem__(self, key: Hashable, value: any) -> None:
        if self.size > self.capacity * self.LOAD_FACTOR:
            self._resize()

        index = self._calculate_index(key)
        if not self.hash_table[index]:
            self.size += 1
        self.hash_table[index] = Dictionary.Node(key, value)

    def __getitem__(self, key: Hashable) -> any:
        index = self._calculate_index(key)
        if self.hash_table[index] is None:
            raise KeyError(f"Key {key} not found")
        return self.hash_table[index].value

    def __len__(self) -> int:
        return self.size

    def clear(self) -> None:
        self.size = 0
        self.hash_table: list[Dictionary.Node | None] = [None] * self.capacity
