from dataclasses import dataclass
from typing import Hashable, Any, Optional


@dataclass
class Node:
    key: Hashable
    value_data: Any
    hash_value: int


class Dictionary:
    initial_capacity = 8
    capacity_multiplier = 2
    size = 0
    load_factor = 2 / 3

    def __init__(self, capacity: int = initial_capacity) -> None:
        self.capacity = capacity
        self._size = 0
        self._hash_table: list[Optional[Node]] = [None] * self.capacity

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return str(self._hash_table)

    def __len__(self) -> int:
        return self._size

    @property
    def max_size(self) -> float:
        return self.capacity * self.load_factor

    def _linear_probing(self, index: int) -> int:
        return (index + 1) % self.capacity

    def _calculate_index(self, key: Hashable) -> int:
        key_hash = hash(key)
        index = key_hash % self.capacity
        while (node := self._hash_table[index]) is not None:
            if node.key == key and node.hash_value == key_hash:
                break
            index = self._linear_probing(index)
        return index

    def _resize(self) -> None:
        print("resize called")
        self.capacity *= self.capacity_multiplier
        old_hash_table = self._hash_table
        self._hash_table = [None] * self.capacity
        self._size = 0
        for node in old_hash_table:
            if node is not None:
                self[node.key] = node.value_data

    def __setitem__(self, key: Hashable, value_data: Any) -> None:
        index = self._calculate_index(key)
        if (node := self._hash_table[index]) is not None:
            node.value_data = value_data
            return

        if self._size >= self.max_size:
            self._resize()
            index = self._calculate_index(key)

        self._hash_table[index] = Node(key=key,
                                       value_data=value_data,
                                       hash_value=hash(key))
        self._size += 1

    def __getitem__(self, key: Hashable) -> Any:
        index = self._calculate_index(key)
        node = self._hash_table[index]
        if node is None:
            raise KeyError(f"No such key: {key}")
        return node.value_data
