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

    def __init__(self, capacity: int = INITIAL_CAPACITY) -> None:
        self.capacity = capacity
        self.length = 0
        self.hash_table: list[None | Node] = [None] * capacity

    def get_index(self, key: Hashable) -> int:
        index = hash(key) % self.capacity
        while (self.hash_table[index] is not None
               and self.hash_table[index].key != key):
            index += 1
            index %= self.capacity
        return index

    def resize(self) -> None:
        hash_table_copy = self.hash_table
        self.__init__(self.capacity * 2)
        for node in hash_table_copy:
            if node:
                self.__setitem__(node.key, node.value)

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.length / self.capacity > self.LOAD_FACTOR:
            self.resize()
        index = self.get_index(key)
        if self.hash_table[index] is None:
            self.hash_table[index] = Node(key, hash(key), value)
            self.length += 1
        else:
            self.hash_table[index].value = value

    def __getitem__(self, key: Hashable) -> Any:
        index = self.get_index(key)
        if self.hash_table[index] is None:
            raise KeyError(f"No such key {key}")
        return self.hash_table[index].value

    def __len__(self) -> int:
        return self.length

    def __delitem__(self, key: Hashable) -> None:
        self[key] = None
        self.length -= 1

    def pop(self, key: Hashable, default: Any = None) -> Any:
        if self[key] is None:
            return default
        value = self[key]
        del self[key]
        self.length -= 1
        return value

    def clear(self) -> None:
        self.hash_table = [None] * self.capacity
        self.length = 0

    def get(self, key: Hashable) -> Any:
        try:
            return self[key]
        except KeyError:
            return None

    def update(self, key: Hashable, value: Any) -> None:
        self[key] = Node(key, hash(key), value)
        self.length += 1

    def __iter__(self) -> None:
        for node in self.hash_table:
            if node is not None:
                yield node.key
