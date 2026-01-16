from dataclasses import dataclass
from typing import Hashable, Any


@dataclass
class Node:
    key: Hashable
    hash_: int
    value: Any


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

    def _max_load(self) -> float:
        return self.capacity * self.LOAD_FACTOR

    def _resize(self) -> None:
        old_hash_table = self._hash_table[:]
        self.capacity *= 2
        self._hash_table = [None] * self.capacity
        self.length = 0
        for item in old_hash_table:
            if item is not None:
                self.__setitem__(item.key, item.value)

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.length > self._max_load():
            self._resize()
        index = self._get_index(key)
        if self._hash_table[index] is None:
            self._hash_table[index] = Node(key, hash(key), value)
            self.length += 1
        else:
            self._hash_table[index].value = value

    def __getitem__(self, key: Hashable) -> Any:
        index = self._get_index(key)
        if self._hash_table[index] is None:
            raise KeyError("No such key")
        return self._hash_table[index].value

    def __len__(self) -> int:
        return self.length

    def __delitem__(self, key: Hashable) -> None:
        index = self._get_index(key)
        if self._hash_table[index] is None:
            raise KeyError("No such key")
        self._hash_table[index] = None
        self.length -= 1

    def clear(self) -> None:
        self.length = 0
        self.capacity = self.INITIAL_CAPACITY
        self._hash_table = [None] * self.capacity
