from __future__ import annotations

from typing import Any, Hashable, Iterator


class Node:
    def __init__(self, key: Hashable, value: Any) -> None:
        self.key = key
        self.value = value
        self.hash = hash(key)

    def __repr__(self) -> str:
        return f"{self.key}:{self.value}(hash-{self.hash})"


class Dictionary:
    def __init__(self, capacity: int = 8, load_factor: float = 2 / 3) -> None:
        self.capacity = capacity
        self.load_factor = load_factor
        self.size = 0
        self.table = [None] * capacity

    def __str__(self) -> str:
        return str(self.table)

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = hash(key) % self.capacity
        node = self.table[index]
        while node is not None:
            if node.hash == hash(key) and node.key == key:
                node.value = value
                return
            index = (index + 1) % self.capacity
            node = self.table[index]
        new_node = Node(key, value)
        self.table[index] = new_node
        self.size += 1
        if self.size > self.capacity * self.load_factor:
            self._resize()

    def __getitem__(self, key: Hashable) -> Any:
        index = hash(key) % self.capacity
        node = self.table[index]
        while node is not None:
            if node.hash == hash(key) and node.key == key:
                return node.value
            index = (index + 1) % self.capacity
            node = self.table[index]
        raise KeyError(key)

    def __delitem__(self, key: Hashable) -> None:
        index = hash(key) % self.capacity
        node = self.table[index]
        prev = None
        while node is not None:
            if node.hash == hash(key) and node.key == key:
                if prev is None:
                    self.table[index] = None
                else:
                    index = (index + 1) % self.capacity
                    node = self.table[index]
                self.size -= 1
                return
            prev = node
            index = (index + 1) % self.capacity
            node = self.table[index]
        raise KeyError(key)

    def __len__(self) -> int:
        return self.size

    def __iter__(self) -> Iterator:
        for node in self.table:
            while node is not None:
                yield node.key

    def clear(self) -> None:
        self.capacity = 8
        self.size = 0
        self.table = [None] * self.capacity

    def get(self, key: Hashable, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    _temp = object()

    def pop(self, key: Hashable, default: Any = _temp) -> Any:
        try:
            value = self[key]
            del self[key]
            return value
        except KeyError:
            if default is not self._temp:
                return default
            raise

    def items(self) -> list[tuple]:
        return [(node.key, node.value,)
                for node in self.table if node is not None]

    def update(self, other: dict | Dictionary | list[tuple]) -> None:
        if isinstance(other, (dict, Dictionary,)):
            for key, value in other.items():
                self[key] = value
        if isinstance(other, list):
            for key, value in other:
                self[key] = value

    def _resize(self) -> None:
        old_table = self.table
        self.capacity *= 2
        self.size = 0
        self.table = [None] * self.capacity
        for node in old_table:
            if node is not None:
                self.__setitem__(node.key, node.value)
