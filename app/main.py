from typing import Hashable, Any, Optional
from dataclasses import dataclass


@dataclass
class Node:
    key: Hashable
    value: Any
    _next: Optional["Node"] = None


class Dictionary:
    def __init__(self) -> None:
        self.capacity: int = 8
        self.hash_table: list[Optional[Node]] = [None] * self.capacity
        self.length: int = 0

    def hash_value(self, key: Hashable) -> int:
        return hash(key) % self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self.hash_value(key)
        node = self.hash_table[index]

        while node:
            if node.key == key:
                node.value = value
                return
            node = node._next

        new_node = Node(key=key, value=value, _next=self.hash_table[index])
        self.hash_table[index] = new_node
        self.length += 1

        if self.length / self.capacity > 0.75:
            self._resize()

    def __contains__(self, key: Hashable) -> bool:
        index = self.hash_value(key)
        node = self.hash_table[index]

        while node:
            if node.key == key:
                return True
            node = node._next
        return False

    def __getitem__(self, key: Hashable) -> Any:
        index = self.hash_value(key)
        node = self.hash_table[index]

        while node:
            if node.key == key:
                return node.value
            node = node._next

        raise KeyError("Key not found in dictionary")

    def __len__(self) -> int:
        return self.length

    def _resize(self) -> None:
        old_hash_table = self.hash_table
        self.capacity *= 2
        self.hash_table = [None] * self.capacity
        self.length = 0

        for node in old_hash_table:
            while node:
                self[node.key] = node.value
                node = node._next
