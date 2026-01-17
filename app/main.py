from dataclasses import dataclass
from typing import Hashable, Any, Optional
from fractions import Fraction


class Dictionary:
    _INITIAL_CAPACITY = 8
    _RESIZE_THRESHOLD = Fraction(2, 3)
    _CAPACITY_MULTIPLIER = 2

    @dataclass
    class Node:
        key: Hashable
        value: Any
        hash_value: int

    def __init__(self) -> None:
        self.capacity = Dictionary._INITIAL_CAPACITY
        self.resize_threshold: Fraction = Dictionary._RESIZE_THRESHOLD
        self.capacity_multyplier: int = Dictionary._CAPACITY_MULTIPLIER
        self.size = 0
        self.hash_table: list[Dictionary.Node | None] = [None] * self.capacity

    def _calculate_index(self, key: Hashable, hash_value: int) -> int:
        index = hash_value % self.capacity

        while (
                self.hash_table[index] is not None
                and self.hash_table[index].key != key
        ):
            index = (index + 1) % self.capacity
        return index

    @property
    def current_max_size(self) -> int:
        return int(self.capacity * self.resize_threshold)

    def resize(self, multiplier: int = None) -> None:
        if multiplier is None:
            multiplier = self.capacity_multyplier

        old_hash_table = self.hash_table
        self.capacity *= multiplier
        self.size = 0
        self.hash_table = [None] * self.capacity

        for node in old_hash_table:
            if node is not None:
                self[node.key] = node.value

    def __setitem__(self, key: Hashable, value: Any) -> None:
        hash_value = hash(key)
        index = self._calculate_index(key, hash_value)

        if self.hash_table[index] is not None:
            self.hash_table[index].value = value
        else:
            self.hash_table[index] = Dictionary.Node(key, value, hash_value)
            self.size += 1

        if self.size >= self.current_max_size:
            self.resize()

    def __getitem__(self, key: Hashable) -> Any:
        hash_value = hash(key)
        index = self._calculate_index(key, hash_value)

        if self.hash_table[index] is None:
            raise KeyError(f"Cannot find value for key: {key}")

        return self.hash_table[index].value

    def __delitem__(self, key: Hashable) -> None:
        hash_value = hash(key)
        index = self._calculate_index(key, hash_value)

        if self.hash_table[index] is None or self.hash_table[index].key != key:
            raise KeyError(f"Cannot find value for key: {key}")

        self.hash_table[index] = None
        self.size -= 1

        self.resize(multiplier=1)

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
        self.hash_table = [None] * self.capacity
        self.size = 0

    def pop(self, key: Hashable, default: Optional[Any] = object()) -> Any:
        hash_value = hash(key)
        index = self._calculate_index(key, hash_value)

        if self.hash_table[index] is None or self.hash_table[index].key != key:
            if default is object():
                raise KeyError(f"Cannot find value for key: {key}")
            return default

        value = self.hash_table[index].value
        self.__delitem__(key)
        return value
