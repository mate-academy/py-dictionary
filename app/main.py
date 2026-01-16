from dataclasses import dataclass
from typing import Hashable, Any


@dataclass
class Node:
    key: Hashable
    value: Any
    hash_: int


class Dictionary:

    INITIAL_CAPACITY = 8
    LOAD_FACTOR = 2 / 3

    def __init__(self) -> None:
        self.capacity = self.INITIAL_CAPACITY
        self.length = 0
        self._hash_table: list[None | Node] = [None] * self.capacity

    def _get_index(self, key: Hashable) -> int:
        hash_ = hash(key)
        index = hash_ % self.capacity

        while (self._hash_table[index] is not None
               and self._hash_table[index].key != key):
            index += 1
            index = index % self.capacity

        return index

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.length == int(self.capacity * self.LOAD_FACTOR):
            self._resize()
        index = self._get_index(key)
        if self._hash_table[index] is None:
            self.length += 1
        self._hash_table[index] = Node(key, value, hash(key))

    def __getitem__(self, key: Hashable) -> Any:
        index = self._get_index(key)

        if self._hash_table[index] is None:
            raise KeyError("No such key")

        return self._hash_table[index].value

    def __len__(self) -> int:
        return self.length

    def _resize(self) -> None:
        self.capacity *= 2
        copy_hash_table = self._hash_table[:]
        self._hash_table = [None] * self.capacity
        for node in copy_hash_table:
            if node is not None:
                index = self._get_index(node.key)
                self._hash_table[index] = node
