from dataclasses import dataclass
from typing import Any, Hashable


@dataclass
class Node:
    key: Hashable
    hash_: int
    value: Any


class Dictionary:
    INITIAL_CAPACITY = 8
    LOAD_FACTOR = 0.66
    RESIZE_MULTIPLIER = 2

    def __init__(self) -> None:
        self.capacity = self.INITIAL_CAPACITY
        self.length = 0
        self.hash_table: list[Node | None] = [None] * self.capacity

    def _get_index(self, key: Hashable, hash_: int) -> int:
        index = hash_ % self.capacity
        while (
            self.hash_table[index] is not None
            and self.hash_table[index].key != key
        ):
            index = (index + 1) % self.capacity
        return index

    def _resize(self) -> None:
        old_nodes = [node for node in self.hash_table if node is not None]
        self.capacity *= self.RESIZE_MULTIPLIER
        self.length = 0
        self.hash_table = [None] * self.capacity
        for node in old_nodes:
            index = self._get_index(node.key, node.hash_)
            self.hash_table[index] = node
            self.length += 1

    def __setitem__(self, key: Hashable, value: Any) -> None:
        hash_ = hash(key)
        index = self._get_index(key, hash_)
        if self.hash_table[index] is None:
            if (self.length + 1) > self.capacity * self.LOAD_FACTOR:
                self._resize()
                index = self._get_index(key, hash_)
            self.hash_table[index] = Node(key, hash_, value)
            self.length += 1
        else:
            self.hash_table[index].value = value

    def __getitem__(self, key: Hashable) -> Any:
        hash_ = hash(key)
        index = self._get_index(key, hash_)
        if self.hash_table[index] is None:
            raise KeyError(f"Key '{key}' not found")
        return self.hash_table[index].value

    def __len__(self) -> int:
        return self.length
