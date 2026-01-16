from dataclasses import dataclass
from typing import Any, Hashable, Optional


class Dictionary:
    @dataclass
    class Node:
        key: Hashable
        value: Any

    def __init__(self, capacity: int = 8) -> None:
        self.capacity = capacity
        self.table: list[Optional[Dictionary.Node]] = [None] * self.capacity
        self.size = 0

    def _find_index(self, key: Hashable) -> int:
        index = hash(key) % self.capacity
        while (
            self.table[index] is not None
            and self.table[index].key != key
        ):
            index = (index + 1) % self.capacity
        return index

    def resize(self) -> None:
        old_hash_table = self.table
        self.capacity *= 2
        self.table = [None] * self.capacity
        self.size = 0

        for node in old_hash_table:
            if node is not None:
                self[node.key] = node.value

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.size + 1 >= self.capacity * (2 / 3):
            self.resize()

        index = self._find_index(key)

        if self.table[index] is None:
            self.size += 1

        self.table[index] = self.Node(key, value)

    def __getitem__(self, key: Any) -> Any:
        index = self._find_index(key)
        if self.table[index] is None:
            raise KeyError(f"Cannot find value for key: {key}")
        return self.table[index].value

    def __len__(self) -> int:
        return self.size
