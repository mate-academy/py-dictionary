from dataclasses import dataclass
from typing import Hashable, Any


@dataclass
class Node:
    key: Hashable
    value: Any
    key_hash: int


class Dictionary:
    INITIAL_CAPACITY = 8
    THRESHOLD = 2 / 3
    CAPACITY_MULTIPLIER = 2

    def __init__(self, capacity: int = INITIAL_CAPACITY) -> None:
        self.capacity = capacity
        self._size = 0
        self._hash_table: list[None | Node] = [None] * self.capacity

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return str(self._hash_table)

    def __len__(self) -> int:
        return self._size

    @property
    def max_size(self) -> float:
        return self.capacity * self.THRESHOLD

    def _linear_probing(self, index: int) -> int:
        return (index + 1) % self.capacity

    def _calculate_index(self, key: Hashable) -> int:
        key_hash = hash(key)
        index = key_hash % self.capacity
        while (node := self._hash_table[index]) is not None:
            if node.key == key and node.key_hash == key_hash:
                break
            index = self._linear_probing(index)
        return index

    def _resize(self) -> None:
        print("resize called")
        self.capacity *= self.CAPACITY_MULTIPLIER
        old_hash_table = self._hash_table
        self._hash_table = [None] * self.capacity
        self._size = 0
        for node in old_hash_table:
            if node is not None:
                self[node.key] = node.value

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self._calculate_index(key)
        node = self._hash_table[index]
        if node is not None:
            node.value = value
            return
        if self._size + 1 >= self.max_size:
            self._resize()
            self[key] = value
        else:
            self._hash_table[index] = Node(key, value, hash(key))
            self._size += 1

    def __getitem__(self, key: Hashable) -> Any:
        index = self._calculate_index(key)
        if (node := self._hash_table[index]) is None:
            raise KeyError(f"No such key: {key}")
        return node.value
