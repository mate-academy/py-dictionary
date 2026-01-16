from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
from typing import Hashable, Any, Iterable, Optional


class Dictionary:
    INITIAL_CAPACITY = 8
    RESIZE_THRESHOLD = Fraction(2, 3)
    CAPACITY_MULTIPLIER = 2

    @dataclass
    class Node:
        key: Hashable
        value: Any
        hash_value: Hashable

    def __init__(self) -> None:
        self.capacity = Dictionary.INITIAL_CAPACITY
        self.size = 0
        self.hash_table: list[Dictionary.Node | None] = [None] * self.capacity

    def _calculate_index(self, key: Hashable) -> int:
        index = hash(key) % self.capacity

        while (
                self.hash_table[index] is not None
                and self.hash_table[index].key != key
        ):
            index = (index + 1) % self.capacity

        return index

    @property
    def current_max_size(self) -> int:
        return round(self.capacity * Dictionary.RESIZE_THRESHOLD)

    def resize(self) -> None:
        old_hash_table = self.hash_table

        self.capacity *= Dictionary.CAPACITY_MULTIPLIER
        self.size = 0
        self.hash_table = [None] * self.capacity

        self.recalculate(old_hash_table)

    def recalculate(
            self,
            old_hash_table: list[Dictionary.Node | None]
    ) -> None:
        for node in old_hash_table:
            if node is not None:
                self[node.key] = node.value

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self._calculate_index(key)

        if self.hash_table[index] is None:
            if self.size + 1 >= self.current_max_size:
                self.resize()
                index = self._calculate_index(key)
            self.size += 1

        self.hash_table[index] = Dictionary.Node(key, value, hash(key))

    def __getitem__(self, key: Hashable) -> Any:
        index = self._calculate_index(key)

        if self.hash_table[index] is None:
            raise KeyError(f"Cannot find key: {key}")

        return self.hash_table[index].value

    def __delitem__(self, key: Hashable) -> None:
        index = self._calculate_index(key)

        if self.hash_table[index] is None:
            raise KeyError(f"Cannot find key: {key}")

        self.hash_table[index] = None
        self.size -= 1
        old_hash_table = self.hash_table
        self.recalculate(old_hash_table)

    def get(self, key: Hashable, default: Optional[Any] = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def __len__(self) -> int:
        return self.size

    def __str__(self) -> str:
        return str(self.hash_table)

    def clear(self) -> None:
        self.capacity = Dictionary.INITIAL_CAPACITY
        self.size = 0
        self.hash_table = [None] * self.capacity

    def pop(self, key: Hashable, default: Optional[Any] = object) -> Any:
        try:
            value = self[key]
        except KeyError as e:
            if default == object:
                raise e
            return default
        self.__delitem__(key)
        return value

    def update(self, other: Dictionary | Iterable = None, **kwargs) -> None:
        if not other and kwargs:
            for key, value in kwargs.items():
                self.__setitem__(key, value)
        elif isinstance(other, Dictionary):
            for node in other.hash_table:
                if node is not None:
                    self[node.key] = node.value
        elif isinstance(other, dict):
            for key, value in other.items():
                self[key] = value
        elif isinstance(other, Iterable):
            for key, value in other:
                self[key] = value
