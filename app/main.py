from __future__ import annotations

from fractions import Fraction
from typing import Any, Iterator, Iterable, Hashable, Optional

NOT_PROVIDED = object()


class Dictionary:
    class Node:
        def __init__(self, key: Any, key_hash: int, value: Any) -> None:
            self.key = key
            self.key_hash = key_hash
            self.value = value

    def __init__(self) -> None:
        self.capacity: int = 8
        self.load_factor: Fraction = Fraction(2, 3)
        self.hash_table: list[Dictionary.Node | None] = [None] * self.capacity
        self.size: int = 0

    def _calculate_index(self, key: Any, hash_key: int) -> int:
        index = hash_key % self.capacity

        while (
            self.hash_table[index] is not None
            and (
                self.hash_table[index].key != key
                or self.hash_table[index].key_hash != hash_key
            )
        ):
            index = (index + 1) % self.capacity

        return index

    @property
    def threshold(self) -> Fraction:
        return self.capacity * self.load_factor

    def __setitem__(self, key: Any, value: Any) -> None:
        index = self._calculate_index(key, hash(key))

        if self.hash_table[index] is None:
            if self.size + 1 >= self.threshold:
                self.resize()
                return self.__setitem__(key, value)
            self.size += 1

        self.hash_table[index] = Dictionary.Node(key, hash(key), value)

    def __getitem__(self, key: Any) -> Any:
        index = self._calculate_index(key, hash(key))

        if self.hash_table[index] is None:
            raise KeyError(f"Key {key} is not in the dict")

        return self.hash_table[index].value

    def __len__(self) -> int:
        return self.size

    def clear(self) -> None:
        self.__init__()

    def __delitem__(self, key: Any) -> None:
        index = self._calculate_index(key, hash(key))

        if self.hash_table[index] is None:
            raise KeyError(f"Cannot find value for key: {key}")

        self.hash_table[index] = None
        self.size -= 1

    def get(self, key: Hashable, default: Optional[Any] = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: Hashable, default: Optional[Any] = NOT_PROVIDED) -> Any:
        try:
            value = self[key]
        except KeyError:
            if default is not NOT_PROVIDED:
                return default
            else:
                raise

        del self[key]
        return value

    def update(self, other: Dictionary | Iterable) -> None:
        for node in other:
            if node:
                self[node.key] = node.value

    def __iter__(self) -> Iterator[Any]:
        return (node for node in self.hash_table if node)

    def resize(self) -> None:
        old_dict = self.hash_table
        self.capacity *= 2
        self.hash_table = [None] * self.capacity
        self.size = 0
        self.update(old_dict)
