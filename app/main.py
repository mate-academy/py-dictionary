from dataclasses import dataclass
from typing import Any


MISSING = object()


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.length = 0
        self.table = [None] * self.capacity

    def __len__(self) -> int:
        return self.length

    def __setitem__(self, key: Any, value: Any) -> None:
        hash_key = hash(key)
        index_key = hash_key % self.capacity
        if self.table[index_key] is None:
            self.table[index_key] = []
        for node in self.table[index_key]:
            if node.key == key:
                node.value = value
                return
        self.table[index_key].append(Node(key, value))
        self.length += 1
        if self.length / self.capacity > 0.75:
            self.resize()

    def __getitem__(self, key: Any) -> Any:
        hash_key = hash(key)
        index_key = hash_key % self.capacity
        cell = self.table[index_key]
        if cell is None:
            raise KeyError(key)
        for node in cell:
            if node.key == key:
                return node.value
        raise KeyError(key)

    def __delitem__(self, key: Any) -> None:
        hash_key = hash(key)
        index_key = hash_key % self.capacity
        cell = self.table[index_key]
        if cell is None:
            raise KeyError(key)
        for i, node in enumerate(cell):
            if node.key == key:
                cell.pop(i)
                self.length -= 1
                return
        raise KeyError(key)

    def get(self, key: Any, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def clear(self) -> None:
        self.table = [None] * self.capacity
        self.length = 0

    def pop(self, key: Any, default: Any = MISSING) -> Any:
        try:
            value = self[key]
            del self[key]
            return value
        except KeyError:
            if default is MISSING:
                raise KeyError(key)
            return default

    def resize(self) -> None:
        old_table = self.table
        self.capacity *= 2
        self.table = [None] * self.capacity
        self.length = 0
        for cell in old_table:
            if cell is not None:
                for node in cell:
                    self[node.key] = node.value


@dataclass
class Node:
    key: object
    value: object

    def __post_init__(self) -> None:
        self.hash = hash(self.key)
