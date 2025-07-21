from __future__ import annotations
from collections.abc import Hashable
from typing import Iterator, Any


class Node:
    def __init__(self, key: Hashable, value: Any) -> None:
        self.key = key
        self.value = value
        self.hash = hash(key)

    def __repr__(self) -> str:
        return f"Node({self.key}, {self.value}, {self.hash})"


class Dictionary:
    def __init__(
            self,
            incoming_data: list[list[Hashable | Any]] = None
    ) -> None:
        self._capacity = 8
        self._load_factor = 0.6
        self._size = 0
        self._hash_table = [None] * self._capacity

        if incoming_data:
            for item in incoming_data:
                if (not isinstance(item, list)) or len(item) != 2:
                    raise ValueError("""Each item must be
                    a list of [key, value]""")
                self.__setitem__(item[0], item[1])

    def __repr__(self) -> str:
        return f"Dictionary({self._hash_table})"

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if not isinstance(key, Hashable):
            raise TypeError(f"unhashable type: {type(key)}")

        index = hash(key) % self._capacity

        while True:
            node = self._hash_table[index]

            if node is None:
                self._hash_table[index] = Node(key, value)
                self._size += 1
                break
            elif node.key == key:
                self._hash_table[index].value = value
                break
            else:
                index = (index + 1) % self._capacity

        if self._size / self._capacity > self._load_factor:
            self._resize()

    def _resize(self) -> None:
        old_table = self._hash_table
        self._capacity *= 2
        self._hash_table = [None] * self._capacity
        self._size = 0

        for node in old_table:
            if node:
                self.__setitem__(node.key, node.value)

    def __getitem__(self, item: Hashable) -> Any:
        index = hash(item) % self._capacity
        while True:
            if self._hash_table[index] is None:
                raise KeyError(f"{item} not found")
            node = self._hash_table[index]
            if node.key == item:
                return node.value
            else:
                index = (index + 1) % self._capacity

    def __len__(self) -> int:
        return self._size

    def clear(self) -> None:
        self._hash_table = [None] * self._capacity
        self._size = 0

    def __delitem__(self, item: Hashable) -> None:
        index = hash(item) % self._capacity
        while True:
            if self._hash_table[index] is None:
                raise KeyError(f"{item} not found")
            node = self._hash_table[index]
            if node.key == item:
                self._hash_table[index] = None
                break
            else:
                index = (index + 1) % self._capacity

        old_table = self._hash_table
        self._hash_table = [None] * self._capacity
        self._size = 0

        for node in old_table:
            if node:
                self.__setitem__(node.key, node.value)

    def get(self, item: Hashable, value_if_error: Any = None) -> Any:
        index = hash(item) % self._capacity
        while True:
            if self._hash_table[index] is None:
                return value_if_error
            node = self._hash_table[index]
            if node.key == item:
                return node.value
            else:
                index = (index + 1) % self._capacity

    def pop(self, item: Hashable) -> Any:
        index = hash(item) % self._capacity
        while True:
            if self._hash_table[index] is None:
                raise KeyError(f"{item} not found")
            node = self._hash_table[index]
            if node.key == item:
                value = node.value
                self.__delitem__(item)
                break
            else:
                index = (index + 1) % self._capacity
        return value

    def update(self, **kwargs) -> None:
        for key, value in kwargs.items():
            self.__setitem__(str(key), value)

    def __iter__(self) -> Iterator[Hashable]:
        return (item.key for item in self._hash_table if item)
