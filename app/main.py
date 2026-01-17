from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
from typing import Hashable, Any, Iterator, Optional, Iterable


class Dictionary:
    @dataclass
    class Node:
        key: Hashable
        value: Any
        key_hash: int

    INITIAL_CAPACITY = 8
    RESIZE_THRESHOLD = Fraction(2, 3)
    CAPACITY_MULTIPLIER = 2

    def __init__(self) -> None:
        self.capacity = self.INITIAL_CAPACITY
        self.size = 0
        self.hash_table: list[Dictionary.Node | None] = [None] * self.capacity

    def _calculate_index(self, key: Hashable) -> int:
        _key_hash = hash(key)
        index = _key_hash % self.capacity

        while (
            self.hash_table[index] is not None
            and (
                self.hash_table[index].key != key
                or self.hash_table[index].key_hash != _key_hash
            )
        ):
            index = (index + 1) % self.capacity

        return index

    @property
    def current_max_size(self) -> int:
        return int(self.capacity * self.RESIZE_THRESHOLD)

    def _resize_up(self) -> None:
        old_hash_table = self.hash_table

        self.capacity *= self.CAPACITY_MULTIPLIER
        self.hash_table = [None] * self.capacity
        self.size = 0

        for node in filter(None, old_hash_table):
            self.__setitem__(node.key, node.value)

    def _resize_down(self) -> None:
        old_hash_table = self.hash_table

        self.capacity //= self.CAPACITY_MULTIPLIER
        self.hash_table = [None] * self.capacity
        self.size = 0

        for node in filter(None, old_hash_table):
            self.__setitem__(node.key, node.value)

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self._calculate_index(key)
        key_hash = hash(key)

        if (
            self.hash_table[index] is not None
            and self.hash_table[index].key == key
        ):
            self.hash_table[index].value = value
            return

        if self.hash_table[index] is None:
            self.size += 1

        self.hash_table[index] = Dictionary.Node(key, value, key_hash)

        if self.size > self.current_max_size:
            self._resize_up()

    def __getitem__(self, key: Hashable) -> Any:
        index = self._calculate_index(key)

        if self.hash_table[index] is None:
            raise KeyError(f"Cannot find value for key: {key}")

        return self.hash_table[index].value

    def __delitem__(self, key: Hashable) -> None:
        index = self._calculate_index(key)

        if self.hash_table[index] is None:
            raise KeyError(f"Cannot delete value for key: {key}")

        self.hash_table[index] = None
        self.size -= 1

        if self.size - 1 < self.current_max_size // self.CAPACITY_MULTIPLIER:
            self._resize_down()

    def __iter__(self) -> Iterator[tuple[Hashable, Any]]:
        for node in self.hash_table:
            if node is not None:
                yield node.key, node.value

    def __len__(self) -> int:
        return self.size

    def __str__(self) -> str:
        items = [
            f"{node.key}: {node.value}"
            for node in self.hash_table
            if node is not None
        ]
        return "{" + ", ".join(items) + "}"

    def __eq__(self, other: Dictionary) -> bool:
        """
        Compare key, value pairs between two Dictionaries.
        """
        if not isinstance(other, Dictionary):
            return False

        if self.size != other.size:
            return False

        for node in self.hash_table:
            if node is not None:
                if other.__getitem__(node.key) != node.value:
                    return False

        return True

    def get(self, key: Hashable, default: Optional[Any] = None) -> Any:
        """
        Get the value for the given key.
        If the key does not exist, return the default value.

        Default value is optional.
        If it was not provided, method will raise KeyError.
        """
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: Hashable, default: Optional[Any] = object()) -> Any:
        try:
            value = self[key]
            self.__delitem__(key)
            return value
        except KeyError:
            if isinstance(default, object):
                return default
            else:
                raise KeyError(
                    f"Cannot delete key: {key} and "
                    "no default value is provided"
                )

    def _update_from_dict(self, data: Dictionary) -> None:
        """
        Updates the dictionary with a Dictionary object.
        """
        for node in data.hash_table:
            if node is not None:
                self.__setitem__(node.key, node.value)

    def _update_from_builtin_dict(self, data: dict) -> None:
        """
        Updates the dictionary with key-value pairs from builtin dictionary.
        """
        for key, value in data.items():
            self.__setitem__(key, value)

    def update(
            self,
            data: Dictionary | list[dict] | dict
    ) -> None:
        """
        Updates Dictionary with various types of data.
        """
        if isinstance(data, Dictionary):
            self._update_from_dict(data)
        elif isinstance(data, dict):
            self._update_from_builtin_dict(data)
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    self._update_from_builtin_dict(item)

    def copy(self) -> Dictionary:
        """
        Creates a copy of the dictionary.
        """
        new_dict = Dictionary()

        for node in self.hash_table:
            if node is not None:
                new_dict.__setitem__(node.key, node.value)

        return new_dict

    def clear(self) -> None:
        """
        Resets the dictionary to its initial state.
        """
        self.capacity = self.INITIAL_CAPACITY
        self.size = 0
        self.hash_table: list[Dictionary.Node | None] = [None] * self.capacity

    @staticmethod
    def from_keys(keys: Iterable, value: Any = None) -> Dictionary:
        """
        Static method to create a new dictionary from keys.
        """
        new_dict = Dictionary()

        for key in keys:
            new_dict.__setitem__(key, value)

        return new_dict
