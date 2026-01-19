from dataclasses import dataclass
from typing import Any, Hashable, Iterator


INITIAL_CAPACITY = 8
RESIZE_THRESHOLD = 2 / 3


@dataclass
class Node:
    key: Hashable
    value: Any


class Dictionary:
    def __init__(self, capacity: int = INITIAL_CAPACITY) -> None:
        self._capacity = capacity
        self._hash_table: list[Node | None] = [None] * self._capacity
        self._size = 0
        self._keys = []

    def _calculate_index(self, key: Hashable) -> int:
        index = hash(key) % self._capacity

        while (
                self._hash_table[index] is not None
                and self._hash_table[index].key != key
        ):
            index = (index + 1) % self._capacity

        return index

    @property
    def _current_max_size(self) -> float:
        return self._capacity * RESIZE_THRESHOLD

    def _resize(self) -> None:
        old_hash_table = self._hash_table
        new_capacity = self._capacity * 2

        self.__init__(new_capacity)

        for node in old_hash_table:
            if node is not None:
                self.__setitem__(node.key, node.value)

    def __setitem__(self, key: Hashable, value: Any) -> None:

        if key not in self._keys:
            self._keys.append(key)

        index = self._calculate_index(key)

        if self._hash_table[index] is None:
            if self._size + 1 >= self._current_max_size:
                self._resize()
                return self.__setitem__(key, value)

            self._size += 1

        self._hash_table[index] = Node(key, value)

    def __getitem__(self, key: Hashable) -> Any:
        index = self._calculate_index(key)

        if self._hash_table[index] is None:
            raise KeyError(f"Cannot find value for key: {key}")

        return self._hash_table[index].value

    def __len__(self) -> int:
        return self._size

    def clear(self) -> None:
        self._hash_table = [None] * self._capacity
        self._size = 0
        self._keys = []

    def __delitem__(self, key: Hashable) -> None:
        index = self._calculate_index(key)

        if self._hash_table[index] is None:
            raise KeyError(f"Cannot find value for key: {key}")

        self._hash_table[index] = None
        self._size -= 1
        self._keys.remove(key)

    def get(self, key: Hashable, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def __str__(self) -> str:
        return str(self._hash_table)

    def pop(self, key: Hashable, default: Any = None) -> Any:
        try:
            index = self._calculate_index(key)
            pop_item = self._hash_table[index].value
            self.__delitem__(key)
            return pop_item
        except KeyError:
            return default

    def __iter__(self) -> Iterator:
        for key in self._keys:
            yield self[key]
