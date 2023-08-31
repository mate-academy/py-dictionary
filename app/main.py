import dataclasses
from typing import Hashable, Any


class Dictionary:
    def __init__(self, capacity: int = 8, load_factor: float = 2 / 3) -> None:
        self.capacity = capacity
        self.load_factor = load_factor
        self.size = 0
        self.table = [None] * self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.size >= self.capacity * self.load_factor:
            self._resize(self.capacity * 2)

        index = self._find_index(key)
        if self.table[index] and self.table[index].key == key:
            self.table[index].value = value
        else:
            node = Node(key, hash(key), value)
            self.table[index] = node
            self.size += 1

    def __getitem__(self, key: Hashable) -> Any:
        index = self._find_index(key)
        if self.table[index] and self.table[index].key == key:
            return self.table[index].value
        raise KeyError(key)

    def _find_index(self, key: Hashable) -> int:
        index = hash(key) % self.capacity
        while self.table[index] and self.table[index].key != key:
            index = (index + 1) % self.capacity
        return index

    def __len__(self) -> int:
        return self.size

    def _resize(self, new_capacity: int) -> None:
        old_table = self.table
        self.capacity = new_capacity
        self.size = 0
        self.table = [None] * new_capacity

        for node in old_table:
            if node:
                self[node.key] = node.value


@dataclasses.dataclass
class Node:
    key: Hashable
    hash_value: int
    value: Any
