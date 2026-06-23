from dataclasses import dataclass
from typing import Any


@dataclass
class Node:
    key: Any
    key_hash: int
    value: Any


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.size = 0
        self.table = [None] * self.capacity

    def __len__(self) -> int:
        return self.size

    def __setitem__(self, key: Any, value: Any) -> None:
        key_hash = hash(key)
        index = key_hash % self.capacity

        while True:
            current_node = self.table[index]

            if current_node is None:
                self.table[index] = Node(key=key,
                                         key_hash=key_hash, value=value)
                self.size += 1

                if self.size / self.capacity > 2 / 3:
                    self._resize()
                return

            if current_node.key == key:
                current_node.value = value
                return

            index = (index + 1) % self.capacity

    def __getitem__(self, key: Any) -> Any:
        key_hash = hash(key)
        index = key_hash % self.capacity

        while True:
            current_node = self.table[index]

            if current_node is None:
                raise KeyError(f"Key {key} not found in Dictionary.")

            if current_node.key == key:
                return current_node.value

            index = (index + 1) % self.capacity

    def _resize(self) -> None:
        old_table = self.table

        self.capacity *= 2
        self.size = 0
        self.table = [None] * self.capacity

        for node in old_table:
            if node is not None:
                self[node.key] = node.value
