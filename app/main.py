from dataclasses import dataclass
from typing import Hashable, Any


@dataclass
class Node:
    key: Hashable
    value: Any
    next_node: "Node" = None


class Dictionary:
    def __init__(self, capacity: int = 8) -> None:
        self.capacity = capacity
        self.size = 0
        self.hash_table = [None] * self.capacity

    def _hash(self, key: Hashable) -> int:
        return hash(key) % self.capacity

    def _find_node(self, key: Hashable) -> tuple:
        index = self._hash(key)
        current = self.hash_table[index]
        prev = None
        while current:
            if current.key == key:
                return current, prev
            prev = current
            current = current.next_node
        return None, prev

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self._hash(key)
        current, _ = self._find_node(key)
        if current:
            current.value = value
        else:
            new_node = Node(key, value, self.hash_table[index])
            self.hash_table[index] = new_node
            self.size += 1
            if self.size / self.capacity > 0.7:
                self._resize()

    def _resize(self) -> None:
        new_capacity = self.capacity * 2
        new_hash_table = [None] * new_capacity
        for i in range(self.capacity):
            current = self.hash_table[i]
            while current:
                new_index = hash(current.key) % new_capacity
                if new_hash_table[new_index] is None:
                    new_hash_table[new_index] = Node(current.key,
                                                     current.value)
                else:
                    new_current = new_hash_table[new_index]
                    while new_current.next_node:
                        new_current = new_current.next_node
                    new_current.next_node = Node(current.key, current.value)
                current = current.next_node
        self.hash_table = new_hash_table
        self.capacity = new_capacity

    def __getitem__(self, item: Hashable) -> Any:
        current, _ = self._find_node(item)
        if current:
            return current.value
        raise KeyError(f"Key '{item}' not in Dictionary")

    def __len__(self) -> int:
        return self.size

    def __delitem__(self, key: Hashable) -> None:
        index = self._hash(key)
        current, prev = self._find_node(key)
        if current:
            if prev:
                prev.next_node = current.next_node
            else:
                self.hash_table[index] = current.next_node
            self.size -= 1
        else:
            raise KeyError(key)

    def get(self, key: Hashable, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError(f"Key '{self[key]}' not in Dictionary"):
            return default

    def pop(self, key: Hashable, default: Any = None) -> Any:
        try:
            value = self[key]
            del self[key]
            return value
        except KeyError:
            if default is None:
                raise KeyError(f"Key '{self[key]}' not in Dictionary")
            return default

    def update(self, other: dict) -> None:
        for key, value in other.items():
            self[key] = value

    def __iter__(self) -> None:
        for _hash in self.hash_table:
            current = _hash
            while current:
                yield current.key
                current = current.next_node

    def items(self) -> None:
        for _hash in self.hash_table:
            current = _hash
            while current:
                yield current.key, current.value
                current = current.next_node
