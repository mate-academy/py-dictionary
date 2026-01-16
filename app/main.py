from dataclasses import dataclass
from typing import Hashable, Any


@dataclass
class Node:
    key: Hashable
    hash_: int
    value: Any


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.length = 0
        self.hash_table: list = [None] * self.capacity
        self.load_factor = 2 / 3

    def __len__(self) -> int:
        return self.length

    def _get_index(self, key: Hashable) -> int:
        hash_number = hash(key)
        index = hash_number % self.capacity
        while (self.hash_table[index] is not None
               and self.hash_table[index].key != key):
            index += 1
            index = index % self.capacity
        return index

    def max_load(self) -> float:
        return self.capacity * self.load_factor

    def _resize(self) -> None:
        old_hash_table = self.hash_table[:]
        self.capacity *= 2
        self.hash_table = [None] * self.capacity
        self.length = 0
        for item in old_hash_table:
            if item is not None:
                self.__setitem__(item.key, item.value)

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.length > self.max_load():
            self._resize()
        index = self._get_index(key)
        if self.hash_table[index] is None:
            self.hash_table[index] = Node(key, hash(key), value)
            self.length += 1
        else:
            self.hash_table[index].value = value

    def __getitem__(self, key: Hashable) -> Any:
        index = self._get_index(key)
        if self.hash_table[index] is None:
            raise KeyError("No such key")
        return self.hash_table[index].value

    def __delitem__(self, key: Hashable) -> None:
        index = self._get_index(key)
        if self.hash_table[index] is None:
            raise KeyError("No such key")
        self.hash_table[index] = None
        self.length -= 1

    def clear(self) -> None:
        self.length = 0
        self.hash_table = [None] * self.capacity
