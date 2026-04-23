from dataclasses import dataclass
from typing import Hashable, Any, Iterator


@dataclass(slots=True)
class Node:
    key: Hashable
    value: Any
    hash_value: int


class CustomDict:
    INITIAL_CAPACITY = 8
    LOAD_FACTOR = 2 / 3
    CAPACITY_MULTIPLIER = 2

    def __init__(self) -> None:
        self._table: list[Node | None] = [None] * self.INITIAL_CAPACITY
        self._size = 0
        self._capacity = self.INITIAL_CAPACITY

    @property
    def _threshold(self) -> Any:
        return self._capacity * self.LOAD_FACTOR

    def _linear_probing(self, index: int) -> int:
        return (index + 1) % self._capacity

    def _calculate_index(self, key: Hashable) -> int:
        hash_value = hash(key)
        index = hash_value % self._capacity
        while (
                (node := self._table[index]) is not None
                and node.hash_value != hash_value
                and node.key != key
        ):
            index = self._linear_probing(index)
        return index

    def _resize(self) -> None:
        old_table = self._table
        self._capacity *= self.CAPACITY_MULTIPLIER
        self._table = [None] * self._capacity
        self._size = 0
        for node in old_table:
            if node is not None:
                self[node.key] = node.value

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self._calculate_index(key)
        if (node := self._table[index]) is None:
            if self._size + 1 > self._threshold:
                self._resize()
                index = self._calculate_index(key)
            self._table[index] = Node(key, value, hash(key))
            self._size += 1
        else:
            node.value = value

    def __getitem__(self, key: Hashable) -> Any:
        index = self._calculate_index(key)
        if (node := self._table[index]) is None:
            raise KeyError
        return node.value

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[Hashable]:
        for node in self._table:
            if node is not None:
                yield node.key

    def get(self, key: Hashable, default: Any = None) -> Any:
        index = self._calculate_index(key)
        node = self._table[index]

        if node is None:
            return default

        return node.value

    def clear(self) -> None:
        self._table = [None] * self.INITIAL_CAPACITY
        self._size = 0
        self._capacity = self.INITIAL_CAPACITY

    def update(self, other: Any) -> None:
        for key, value in other:
            self[key] = value

    def pop(self, key: Hashable, default: Any = None) -> Any:
        try:
            value = self[key]
            del self[key]
            return value
        except KeyError:
            if default is not None:
                return default
            raise KeyError(key)

    def __delitem__(self, key: Hashable) -> None:
        index = self._calculate_index(key)

        if self._table[index] is None:
            raise KeyError(key)

        self._table[index] = None
        self._size -= 1

        next_index = self._linear_probing(index)

        while self._table[next_index] is not None:
            node_to_rehash = self._table[next_index]
            self._table[next_index] = None
            self._size -= 1
            self[node_to_rehash.key] = node_to_rehash.value
            next_index = self._linear_probing(next_index)
