from typing import Any, List
from dataclasses import dataclass


@dataclass
class Node:
    key: str
    hash_: int
    value: Any

    def __str__(self) -> str:
        return f"{self.key}: {self.value}"

    def __repr__(self) -> str:
        return f"{self.key}: {self.value}"


class Dictionary:
    def __init__(
        self, initial_capacity: int = 8, load_factor: float = 2 / 3
    ) -> None:
        self._length = 0
        self._capacity = initial_capacity
        self._load_factor = load_factor
        self._hash_table: List[Node | None] = [None] * self._capacity

    def clear(self) -> None:
        self._hash_table = [None] * self._capacity
        self._length = 0

    def _find_index(self, key: str) -> int:
        _hash = hash(key)
        index = _hash % self._capacity
        while self._hash_table[index] is not None and (
            self._hash_table[index].hash_ != _hash
            or self._hash_table[index].key != key
        ):
            index = (index + 1) % self._capacity
        return index

    def _set_node(self, node: Node) -> None:
        index = self._find_index(node.key)
        if self._hash_table[index] is None:
            self._length += 1
        self._hash_table[index] = node

    def _resize(self) -> None:
        old_hash_table = self._hash_table
        self._capacity *= 2
        self._hash_table = [None] * self._capacity
        self._length = 0
        for node in old_hash_table:
            if node is not None:
                self._set_node(node)

    def __setitem__(self, key: Any, value: Any) -> None:
        node = Node(key, hash(key), value)
        if (self._length / self._capacity) >= self._load_factor:
            self._resize()
        self._set_node(node)

    def __getitem__(self, key: str) -> str:
        index = self._find_index(key)
        if self._hash_table[index] is None:
            raise KeyError
        return self._hash_table[index].value

    def __delitem__(self, key: str) -> None:
        index = self._find_index(key)
        if self._hash_table[index] is not None:
            self._hash_table[index] = None
            self._length -= 1

    def get(self, key: str, default: Any = None) -> Any:
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def pop(self, default: Any = None) -> Any:
        if self._length != 0:
            index = self._capacity - 1
            while self._hash_table[index] is None:
                index -= 1
            self._length -= 1
            node = self._hash_table[index]
            self._hash_table[index] = None
            return node.value
        return default

    def __iter__(self) -> iter:
        for node in self._hash_table:
            if node is not None:
                yield node.key

    def items(self) -> list[tuple]:
        return [(key, self.__getitem__(key=key)) for key in self]

    def update(
        self, other: "Dictionary" = None, *args: list, **kwargs: dict
    ) -> None:
        if other is None:
            pass
        else:
            items = other.items() if hasattr(other, "items") else other
            for key, value in items:
                self.__setitem__(key, value)
        for key, value in args:
            self.__setitem__(key, value)
        for key, value in kwargs.items():
            self.__setitem__(key, value)

    def __str__(self) -> str:
        key_values = [
            key_value
            for key_value in self._hash_table
            if key_value is not None
        ]
        return str(key_values)

    def __len__(self) -> int:
        return self._length
