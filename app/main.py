from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Hashable, Iterable, Optional, Generator


class Dictionary:
    @dataclass
    class Node:
        key: Hashable
        k_hash: int
        value: Any

    INITIAL_CAPACITY = 8
    LOAD_FACTOR = Fraction(2, 3)
    CAPACITY_MULTIPLIER = 2
    _NOT_PROVIDED = object()

    def __init__(self) -> None:
        try:
            self.capacity
        except AttributeError:
            self.capacity = Dictionary.INITIAL_CAPACITY
        self.hashtable: list[Dictionary.Node | None] = [None] * self.capacity
        self.size = 0
        self.keys = []

    def get_index(self, key: Hashable) -> int:
        index = hash(key) % self.capacity

        while (
            self.hashtable[index] is not None
            and self.hashtable[index].key != key
        ):
            index = (index + 1) % self.capacity

        return index

    @property
    def resize_threshold(self) -> Fraction:
        return self.capacity * Dictionary.LOAD_FACTOR

    def __getitem__(self, key: Hashable) -> Any:
        index = self.get_index(key)

        if self.hashtable[index] is None:
            raise KeyError(f"{key}")

        return self.hashtable[index].value

    def resize(self) -> None:
        old_hash_table = self.hashtable

        self.capacity *= Dictionary.CAPACITY_MULTIPLIER
        self.__init__()

        for node in old_hash_table:
            if node is not None:
                self.__setitem__(node.key, node.value)

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self.get_index(key)

        if self.hashtable[index] is None:
            if self.size + 1 >= self.resize_threshold:
                self.resize()
                index = self.get_index(key)
            self.size += 1
            self.keys.append(key)

        self.hashtable[index] = Dictionary.Node(key, hash(key), value)

    def __len__(self) -> int:
        return self.size

    def __delitem__(self, key: Hashable) -> None:
        index = self.get_index(key)

        if self.hashtable[index] is None:
            raise KeyError(f"{key}")

        self.hashtable[index] = None
        self.keys.remove(key)
        self.size -= 1

    def clear(self) -> None:
        self.__init__()
        self.keys = []

    def get(self, key: Hashable, default: Optional[Any] = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def pop(
            self,
            key: Hashable,
            default: Optional[Any] = _NOT_PROVIDED
    ) -> Any:
        try:
            value = self[key]
        except KeyError:
            if default is not Dictionary._NOT_PROVIDED:
                return default
            raise KeyError(f"{key}")
        else:
            del self[key]
            return value

    def update(
            self,
            other: Dictionary | Iterable = _NOT_PROVIDED
    ) -> None:
        if other == Dictionary._NOT_PROVIDED:
            return
        if isinstance(other, Dictionary):
            for node in other:
                self.__setitem__(node.key, node.value)

        elif isinstance(other, Iterable):
            for item in other:
                if isinstance(item, (list, tuple)) and len(item) == 2:
                    key, value = item
                    self.__setitem__(key, value)
                else:
                    raise ValueError(
                        "Iterable must contain pairs of (key, value)"
                    )
        else:
            raise TypeError(
                f"Expected a dict or iterable of pairs, "
                f"got {type(other).__name__}"
            )

    def __iter__(self) -> Generator:
        self.current_key = 0
        while self.current_key < len(self.keys):
            index = self.get_index(self.keys[self.current_key])
            self.current_key += 1
            yield self.hashtable[index].key
