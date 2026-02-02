from dataclasses import dataclass
from typing import Hashable


@dataclass
class Node:
    key: Hashable
    hash_: int
    value: any


class Dictionary:
    pass
    INITIAL_CAPACITY = 8
    LOAD_FACTOR = 2 / 3

    def __init__(self, capacity: int = INITIAL_CAPACITY) -> None:
        self.capacity = capacity
        self.length = 0
        self._hash_table: list[Node | None] = [None] * capacity

    def _get_index(self, key: Hashable) -> int:
        hash_ = hash(key)
        index = hash_ % self.capacity

        while (self._hash_table[index] is not None
               and self._hash_table[index].key != key):
            index = (index + 1) % self.capacity

        return index

    def _resize(self) -> None:
        old_hash_table = self._hash_table
        self.capacity *= 2
        self._hash_table = [None] * self.capacity
        self.length = 0

        for node in old_hash_table:
            if node is not None:
                self.__setitem__(node.key, node.value)

    def __setitem__(self, key: Hashable, value: any) -> None:
        if self.length / self.capacity >= self.LOAD_FACTOR:
            self._resize()

        index = self._get_index(key)

        if self._hash_table[index] is None:
            self._hash_table[index] = Node(key, hash(key), value)
            self.length += 1
        else:
            self._hash_table[index].value = value

    def __getitem__(self, key: Hashable) -> any:
        index = self._get_index(key)

        if self._hash_table[index] is None:
            raise KeyError(f"No such key: {key}")
        return self._hash_table[index].value

    def __len__(self) -> int:
        return self.length

    def clear(self) -> None:
        self._hash_table = [None] * self.capacity
        self.capacity = self.INITIAL_CAPACITY
        self.length = 0

    def __delitem__(self, key: Hashable) -> None:
        index = self._get_index(key)

        if self._hash_table[index] is None:
            raise KeyError(f"No such key: {key}")

        self._hash_table[index] = None
        self.length -= 1
        next_index = (index + 1) % self.capacity

        while self._hash_table[next_index] is not None:
            node = self._hash_table[next_index]
            self._hash_table[next_index] = None
            self.length -= 1
            self[node.key] = node.value
            next_index = (next_index + 1) % self.capacity

    def get(self, key: Hashable, default: any = None) -> any:
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: Hashable, default: any = None) -> any:
        try:
            value = self[key]
            del self[key]
            return value
        except KeyError:
            if default is None:
                raise KeyError(f"Element '{key}' not found")
            return default

    def update(self, **kwargs) -> None:
        for key, value in kwargs.items():
            self[key] = value

    def __iter__(self) -> any:
        for node in self._hash_table:
            if node is not None:
                yield node.key

    def items(self) -> any:
        for node in self._hash_table:
            if node is not None:
                yield node.key, node.value

    def __str__(self) -> str:
        return "; ".join(f"{element.key}: {element.value}"
                         for element in self._hash_table
                         if element is not None)
