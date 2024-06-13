import dataclasses
from typing import Hashable, Any, Optional


@dataclasses.dataclass
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
        self.hash_table: list[Optional[Node]] = [None] * capacity

    def _get_index(
            self,
            key: Hashable,
            hash_table: Optional[list[Optional[Node]]] = None
    ) -> int:
        if hash_table is None:
            hash_table = self.hash_table
        capacity = len(hash_table)
        hash_ = hash(key)
        index = hash_ % capacity

        while (
            hash_table[index] is not None
            and hash_table[index].key != key
        ):
            index = (index + 1) % capacity

        return index

    def _resize(self) -> None:
        new_capacity = self.capacity * 2
        new_hash_table = [None] * new_capacity

        for node in self.hash_table:
            if node is not None:
                index = self._get_index(node.key, new_hash_table)
                new_hash_table[index] = node

        self.capacity = new_capacity
        self.hash_table = new_hash_table

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.length / self.capacity > self.LOAD_FACTOR:
            self._resize()

        index = self._get_index(key)
        if self.hash_table[index] is None:
            self.hash_table[index] = Node(key, hash(key), value)
            self.length += 1
        else:
            self.hash_table[index].value = value

    def __getitem__(self, key: Hashable) -> Any:
        index = self._get_index(key)
        if self.hash_table[index] is not None:
            return self.hash_table[index].value
        raise KeyError(f"Key {key} not found")

    def __delitem__(self, key: Hashable) -> None:
        index = self._get_index(key)
        if self.hash_table[index] is not None:
            self.hash_table[index] = None
            self.length -= 1
            next_index = (index + 1) % self.capacity
            while self.hash_table[next_index] is not None:
                node = self.hash_table[next_index]
                self.hash_table[next_index] = None
                self.length -= 1
                self.__setitem__(node.key, node.value)
                next_index = (next_index + 1) % self.capacity
        else:
            raise KeyError(f"Key {key} not found")

    def __len__(self) -> int:
        return self.length

    def __iter__(self) -> None:
        for node in self.hash_table:
            if node is not None:
                yield node.key

    def clear(self) -> None:
        self.hash_table = [None] * self.capacity
        self.length = 0

    def get(self, key: Hashable, default: Optional[Any] = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: Hashable, default: Optional[Any] = None) -> Any:
        try:
            value = self[key]
            del self[key]
            return value
        except KeyError:
            if default is None:
                raise
            return default

    def update(self, other: "Dictionary") -> None:
        for key in other:
            self[key] = other[key]
