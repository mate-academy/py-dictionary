from __future__ import annotations
from dataclasses import dataclass
from typing import Hashable, Any, Optional


@dataclass
class Node:
    key: Hashable
    hash_: int
    value: Any


class Dictionary:
    INITIAL_CAPACITY = 8
    LOAD_FACTOR = 2 / 3

    def __init__(self, capacity: int = INITIAL_CAPACITY) -> None:
        self.capacity = capacity
        self.length = 0
        self._hash_table: list[Optional[Node]] = [None] * capacity

    def _get_index(self, key: Hashable) -> int:
        hash_ = hash(key)
        index = hash_ % self.capacity
        while (self._hash_table[index] is not None
               and self._hash_table[index].key != key):
            index += 1
            index %= self.capacity
        return index

    def _resize(self) -> None:
        old_hash_table = self._hash_table
        self.capacity *= 2
        self.length = 0
        self._hash_table = [None] * self.capacity

        for element in old_hash_table:
            if element is not None:
                self[element.key] = element.value

    def __setitem__(self, key: Hashable, value: Any) -> None:
        hash_value = hash(key)
        index = self._get_index(key)

        if self._hash_table[index] is None:
            if self.length >= int(self.LOAD_FACTOR * self.capacity):
                self._resize()
                index = self._get_index(key)

            self._hash_table[index] = Node(key, hash_value, value)
            self.length += 1
        else:
            self._hash_table[index].value = value

    def __getitem__(self, key: Hashable) -> Any:
        index = self._get_index(key)

        if self._hash_table[index] is None:
            raise KeyError(f"No such key: {key}")

        return self._hash_table[index].value

    def __delitem__(self, key: Hashable) -> None:
        index = self._get_index(key)

        if self._hash_table[index] is None:
            raise KeyError(f"No such key: {key}")

        self._hash_table[index] = None
        self.length -= 1
        self._rehash_from(index)

    def _rehash_from(self, start_index: int) -> None:
        index = (start_index + 1) % self.capacity
        while self._hash_table[index] is not None:
            node = self._hash_table[index]
            self._hash_table[index] = None
            self.length -= 1
            self[node.key] = node.value
            index = (index + 1) % self.capacity

    def clear(self) -> None:
        self.__init__()

    def get(self, key: Hashable, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def __len__(self) -> int:
        return self.length

    def pop(self, key: Hashable, default: Any = None) -> Any:
        if key in self:
            value = self[key]
            del self[key]
            return value
        if default is not None:
            return default
        raise KeyError(f"No such key: {key}")

    def update(self, other: Dictionary | dict) -> None:
        for key, value in other.items():
            self[key] = value
