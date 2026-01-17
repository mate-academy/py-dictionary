from dataclasses import dataclass
from typing import Any, Hashable, List, Optional, Iterator


INITIAL_CAPACITY = 8
LOAD_FACTOR = 0.75


@dataclass
class Node:
    key: Hashable
    value: Any
    _hash: int


class Dictionary:
    def __init__(self, capacity: int = INITIAL_CAPACITY) -> None:
        self.capacity = capacity
        self.size = 0
        self.hash_table: List[Optional[Node]] = [None] * self.capacity

    def calculate_index(self, key: Hashable, key_hash: int) -> int:
        index = key_hash % self.capacity
        while (
                self.hash_table[index] is not None
                and self.hash_table[index].key != key
        ):
            index = (index + 1) % self.capacity
        return index

    def resize(self) -> None:
        old_hash_table = self.hash_table
        self.capacity *= 2
        self.hash_table = [None] * self.capacity
        self.size = 0

        for node in old_hash_table:
            if node is not None:
                self.__setitem__(node.key, node.value)

    def __setitem__(self, key: Hashable, value: Any) -> None:
        key_hash = hash(key)
        index = self.calculate_index(key, key_hash)

        if self.hash_table[index] is None:
            if self.size + 1 > self.capacity * LOAD_FACTOR:
                self.resize()
                return self.__setitem__(key, value)
            self.size += 1

        self.hash_table[index] = Node(key, value, key_hash)

    def __getitem__(self, key: Hashable) -> Any:
        key_hash = hash(key)
        index = self.calculate_index(key, key_hash)
        node = self.hash_table[index]

        if node is None or node.key != key:
            raise KeyError(f"Key not found: {key}")

        return node.value

    def __len__(self) -> int:
        return self.size

    def clear(self) -> None:
        self.hash_table = [None] * self.capacity
        self.size = 0

    def __delitem__(self, key: Hashable) -> None:
        key_hash = hash(key)
        index = self.calculate_index(key, key_hash)
        node = self.hash_table[index]

        if node is None or node.key != key:
            raise KeyError(f"Key not found: {key}")

        self.hash_table[index] = None
        self.size -= 1

        # Rehash elements to prevent lookup issues
        next_index = (index + 1) % self.capacity
        while self.hash_table[next_index] is not None:
            rehash_node = self.hash_table[next_index]
            self.hash_table[next_index] = None
            self.size -= 1
            self.__setitem__(rehash_node.key, rehash_node.value)
            next_index = (next_index + 1) % self.capacity

    def get(self, key: Hashable, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: Hashable) -> Any:
        value = self[key]
        del self[key]
        return value

    def update(self, other: dict) -> None:
        for key, value in other.items():
            self[key] = value

    def __iter__(self) -> Iterator[Hashable]:
        for node in self.hash_table:
            if node is not None:
                yield node.key

    def __str__(self) -> str:
        items = [f"{node.key}: {node.value}"
                 for node in self.hash_table
                 if node is not None]
        return "{" + ", ".join(items) + "}"
