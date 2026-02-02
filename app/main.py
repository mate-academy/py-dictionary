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

        while (
            self._hash_table[index] is not None
            and self._hash_table[index].key != key
        ):
            index = (index + 1) % self.capacity
        return index

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.length / self.capacity >= self.LOAD_FACTOR:
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
            raise KeyError(f"No such key: {key}")
        return self._hash_table[index].value

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
            self.__setitem__(node.key, node.value)
            next_index = (next_index + 1) % self.capacity

    def __len__(self) -> int:
        return self.length

    def _resize(self) -> None:
        old_hash_table = self._hash_table
        self.capacity *= 2
        self._hash_table = [None] * self.capacity
        self.length = 0

        for node in old_hash_table:
            if node is not None:
                self.__setitem__(node.key, node.value)

    def clear(self) -> None:
        self._hash_table = [None] * self.capacity
        self.length = 0

    def get(self, key: Hashable, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: Hashable, default: Any = None) -> Any:
        try:
            value = self.__getitem__(key)
            self.__delitem__(key)
            return value
        except KeyError:
            if default is None:
                raise
            return default

    def update(self, **kwargs) -> None:
        for key, value in kwargs.items():
            self.__setitem__(key, value)

    def __iter__(self) -> Any:
        for node in self._hash_table:
            if node is not None:
                yield node.key

    def items(self) -> Any:
        for node in self._hash_table:
            if node is not None:
                yield node.key, node.value
