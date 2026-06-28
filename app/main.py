from __future__ import annotations

from random import choice
from typing import Any


class Node:
    def __init__(self, key: Any, value: Any, hash_value: int = None) -> None:
        self._key = key
        self._value = value
        self._hash_value = hash(key) if not hash_value else hash_value

    @property
    def key(self) -> Any:
        return self._key

    @key.setter
    def key(self, key: Any) -> None:
        self._key = key

    @property
    def value(self) -> Any:
        return self._value

    @value.setter
    def value(self, value: Any) -> None:
        self._value = value

    def __repr__(self) -> str:
        return f"{self.key} (#{self.hash_value}): {self.value}"

    @property
    def hash_value(self) -> Any:
        return self._hash_value


class Dictionary:
    load_factor: float = 2 / 3
    growth_factor: int = 2
    initial_size: int = 8

    def __init__(self) -> None:
        self.length = 0
        self.hash_table: list = [None] * self.initial_size

    def __len__(self) -> int:
        return self.length

    def __repr__(self) -> str:
        return ", ".join([str(node) for node in self.hash_table])

    def calculate_index(self, hash_value: int) -> int:
        return hash_value % len(self.hash_table)

    @staticmethod
    def calculate_hash(key: Any) -> int:
        return hash(key)

    def __setitem__(self, key: Any, value: Any) -> None:
        hash_value: int = self.calculate_hash(key)
        index = self.calculate_index(hash_value)
        if self.hash_table[index]:
            if self.hash_table[index].key == key:
                self.hash_table[index].value = value
                return
            for node in self.hash_table:
                if node and node.key == key:
                    node.value = value
                    return
        if int(self.load_factor * len(self.hash_table)) == self.length:
            temp_table = self.hash_table[:]
            self.hash_table: list \
                = [None] * self.growth_factor * len(self.hash_table)
            self.length = 0
            for cell in temp_table:
                if cell:
                    self.__setitem__(cell.key, cell.value)
        if self.hash_table[index]:
            empty_cells = []
            for ind, node in enumerate(self.hash_table):
                if not node:
                    empty_cells.append(ind)
            index = choice(empty_cells)
        self.hash_table[index] = Node(key, value, hash_value)
        self.length += 1

    def __getitem__(self, key: Any) -> Any:
        hash_value: int = self.calculate_hash(key)
        for index in (
                self.calculate_index(hash_value), *range(len(self.hash_table))
        ):
            if self.hash_table[index] and self.hash_table[index].key == key:
                return self.hash_table[index].value
        raise KeyError(f"{key}")

    def __delitem__(self, key: Any) -> None:
        hash_value: int = self.calculate_hash(key)
        for index in (
                self.calculate_index(hash_value), *range(len(self.hash_table))
        ):
            if self.hash_table[index] and self.hash_table[index].key == key:
                self.hash_table[index] = None
                return
        raise KeyError(f"{key}")

    def get(self, key: Any, default_value: Any = None) -> Any:
        try:
            return self.__getitem__(key)
        except KeyError:
            return default_value

    def pop(self, key: Any, default_value: Any = None) -> Any:
        try:
            result = self.__getitem__(key)
            self.__delitem__(key)
            return result
        except KeyError:
            return default_value

    def __iter__(self) -> Dictionary:
        self.iter_index = 0
        return self

    def __next__(self) -> Node:
        while True:
            if self.iter_index >= len(self.hash_table):
                raise StopIteration
            next_node = self.hash_table[self.iter_index]
            self.iter_index += 1
            if next_node:
                break
        return next_node

    def update(self, *keys_values: tuple | list) -> None:
        for key, value in keys_values:
            self.__setitem__(key, value)
