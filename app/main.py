from __future__ import annotations
from typing import Hashable, Union, Any
from dataclasses import dataclass


@dataclass
class Node:
    hash_: int
    key: Hashable
    value: Any


class Dictionary:
    def __init__(self) -> None:
        self._capacity = 8
        self._hash_table: list[Union[None, Node]] = [None] * self._capacity
        self._length = 0
        self._load_factor = 2 / 3

    def __len__(self) -> int:
        return self._length

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self._find_index(key)

        self._add_items_to_hash_table(index, key, value)
        if self._hash_table_is_overloaded():
            self._resize()

    def __getitem__(self, key: Hashable) -> Any:
        index = self._find_index(key)
        self._check_key_exists(index, key)
        return self._hash_table[index].value

    def __delitem__(self, key: Hashable) -> None:
        index = self._find_index(key)
        if self._hash_table[index] is not None:
            self._delete_items(index)

    def pop(self, key: Hashable, *args) -> Any:
        if len(args) > 1:
            raise TypeError
        index = self._find_index(key)
        if self._hash_table[index] is not None:
            return self._delete_items(index)
        elif len(args) == 1:
            return args[0]
        raise KeyError(f"key {key} is not found")

    def get(self, key: Hashable, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def clear(self) -> None:
        self._hash_table = [None] * self._capacity
        self._length = 0

    def update(self, expand: Any) -> None:
        dictionary = expand if isinstance(
            expand, Dictionary
        ) else self._convert_to_dict(expand)

        for element in dictionary._hash_table:
            if element is not None:
                self[element.key] = element.value

    def __iter__(self) -> iter:
        for items in self._hash_table:
            if items is not None:
                yield items.key

    def _find_index(self, key: Hashable) -> int:
        hash_ = hash(key)
        index = hash_ % self._capacity

        while (
            self._hash_table[index] is not None
            and (
                self._hash_table[index].hash_ != hash_
                or self._hash_table[index].key != key
            )
        ):
            index += 1
            index %= self._capacity

        return index

    def _add_items_to_hash_table(
            self,
            index: int,
            key: Hashable,
            value: Any
    ) -> None:
        if self._hash_table[index] is None:
            self._length += 1
        self._hash_table[index] = Node(hash(key), key, value)

    def _hash_table_is_overloaded(self) -> bool:
        return self._length >= self._capacity * self._load_factor

    def _check_key_exists(self, index: int, key: Hashable) -> None:
        if self._hash_table[index] is None:
            raise KeyError(f"Key {key} is not present in the hash table")

    def _resize(self) -> None:
        self._capacity *= 2
        self._length = 0
        old_hash_table = self._hash_table
        self._hash_table = [None] * self._capacity

        for items in old_hash_table:
            if items is not None:
                self[items.key] = items.value

    def _delete_items(self, index: int) -> Any:
        value = self._hash_table[index].value
        self._hash_table[index] = None
        self._length -= 1
        return value

    @staticmethod
    def _convert_to_dict(obj: Any) -> Dictionary:
        dictionary = Dictionary()
        for pairs in obj:
            dictionary[pairs[0]] = pairs[1]
        return dictionary
