from collections.abc import Hashable
from typing import Any
from dataclasses import dataclass


@dataclass
class Node:
    key: Hashable
    value: Any
    hash_value: int


class Dictionary:
    def __init__(self,
                 capacity: int = 8,
                 load_factor_threshold: float = 0.7) -> None:
        self._capacity = capacity
        self._load_factor_threshold = load_factor_threshold
        self._table = [[] for _ in range(self._capacity)]
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def _get_hash_and_index(self,
                            key: Hashable) -> tuple[int, int]:
        hash_key = hash(key)
        index = hash_key % len(self._table)
        return hash_key, index

    def __setitem__(self,
                    key: Hashable,
                    value: Hashable) -> None:
        if self._size / len(self._table) > self._load_factor_threshold:
            self.resize()
        hash_key, index = self._get_hash_and_index(key)
        for i, node in enumerate(self._table[index]):
            if node.key == key:
                self._table[index][i] = Node(key, value, hash_key)
                break
        else:
            self._table[index].append(Node(key, value, hash_key))
            self._size += 1

    def __getitem__(self,
                    key: Hashable) -> Any:
        hash_key, index = self._get_hash_and_index(key)
        for node in self._table[index]:
            if node.key == key:
                return node.value
        raise KeyError(key)

    def resize(self) -> None:
        new_capacity = len(self._table) * 2
        new_table = [[] for _ in range(new_capacity)]
        for bucket in self._table:
            for node in bucket:
                new_index = node.hash_value % new_capacity
                new_table[new_index].append(node)
        self._table = new_table
        self._capacity = new_capacity

    def __delitem__(self, key: Hashable) -> None:
        hash_key, index = self._get_hash_and_index(key)
        for i, node in enumerate(self._table[index]):
            if node.key == key:
                del self._table[index][i]
                self._size -= 1
                return
        raise KeyError(key)

    def clear(self) -> None:
        self._table = [[] for _ in range(len(self._table))]
        self._size = 0
