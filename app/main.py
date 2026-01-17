from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Hashable, Optional, Iterator, Iterable


class Dictionary:
    _INITIAL_CAPACITY = 8
    _LOAD_FACTOR = Fraction(2, 3)
    _CAPACITY_MULTIPLIER = 2

    _sentinel = object()

    @dataclass
    class Node:
        key: Hashable
        key_hash: int
        value: Any

    def __init__(self) -> None:
        self._capacity = self._INITIAL_CAPACITY
        self._threshold = int(self._capacity * self._LOAD_FACTOR)
        self._size = 0
        self._hash_table: list[Dictionary.Node | None] = (
            [None] * self._capacity
        )

    def _calculate_index(self, key: Hashable) -> int:
        index = hash(key) % self._capacity

        while (
                self._hash_table[index] is not None
                and self._hash_table[index].key != key
        ):
            index = (index + 1) % self._capacity

        return index

    def __getitem__(self, key: Hashable) -> Any:
        item: Dictionary.Node | None = (
            self._hash_table[self._calculate_index(key)]
        )

        if not item:
            raise KeyError(f"'{key}'")

        return item.value

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self._calculate_index(key)

        if not self._hash_table[index]:
            if self._size + 1 >= self._threshold:
                self._resize_hash_table()
                index = self._calculate_index(key)
            self._hash_table[index] = Dictionary.Node(key, hash(key), value)
            self._size += 1
        else:
            self._hash_table[index].value = value

    def __delitem__(self, key: Hashable) -> None:
        index = self._calculate_index(key)

        if not self._hash_table[index]:
            raise KeyError(f"'{key}'")

        self._hash_table[index] = None
        self._size -= 1

        next_index = (index + 1) % self._capacity
        while self._hash_table[next_index] is not None:
            item = self._hash_table[next_index]
            self._hash_table[next_index] = None
            self._size -= 1

            reindex = self._calculate_index(item.key)
            while self._hash_table[reindex]:
                reindex = (reindex + 1) % self._capacity
            self._hash_table[reindex] = item
            self._size += 1

            next_index = (next_index + 1) % self._capacity

    def __iter__(self) -> Iterator[Hashable]:
        return (item.key for item in self._hash_table if item)

    def __len__(self) -> int:
        return self._size

    def __str__(self) -> str:
        return str(self._hash_table)

    def _resize_hash_table(self) -> None:
        previous_hash_table = self._hash_table

        self._capacity *= self._CAPACITY_MULTIPLIER
        self._threshold = int(self._capacity * self._LOAD_FACTOR)
        self._size = 0
        self._hash_table: list[Dictionary.Node | None] = (
            [None] * self._capacity
        )

        for node in previous_hash_table:
            if node:
                self[node.key] = node.value

    def clear(self) -> None:
        self._size = 0
        self._hash_table = [None] * self._capacity

    def get(self, key: Hashable,
            default_value: Optional[Any] = _sentinel) -> Any:
        try:
            return self[key]
        except KeyError:
            if default_value is self._sentinel:
                raise
            return default_value

    def pop(self, key: Hashable,
            default_value: Optional[Any] = _sentinel) -> Any:
        try:
            item = self[key]
            del self[key]
            return item.value
        except KeyError:
            if default_value is self._sentinel:
                raise
            return default_value

    def keys(self) -> list[Hashable]:
        return [
            item.key
            for item in self._hash_table
            if isinstance(item, Dictionary.Node)
        ]

    def values(self) -> list[Any]:
        return [
            item.value
            for item in self._hash_table
            if isinstance(item, Dictionary.Node)
        ]

    def items(self) -> list[tuple[Hashable, Any]]:
        return [
            (item.key, item.value)
            for item in self._hash_table
            if isinstance(item, Dictionary.Node)
        ]

    def update(
            self,
            other: Dictionary | Iterable[Hashable, Any] = None
    ) -> None:
        if isinstance(other, Dictionary):
            for key, value in other.items():
                self[key] = value
        else:
            try:
                for key, value in other:
                    self[key] = value
            except (TypeError, ValueError) as e:
                raise TypeError(
                    "Expected Dictionary or iterable of key-value pairs."
                ) from e
