from __future__ import annotations

from typing import Any, Hashable, Iterator

from dataclasses import dataclass


@dataclass
class Node:
    hash: int
    key: Hashable
    value: Any


class Dictionary:

    def __init__(self) -> None:
        self.__size = 0
        self.__capacity = 8
        self._hash_table: list[Node | None] = [None] * self.__capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        key_hash = hash(key)
        hash_index = self.__index_to_write(key)
        if self._hash_table[hash_index] is None:
            self.__size += 1
        node = Node(hash=key_hash, key=key, value=value)
        self._hash_table[hash_index] = node

        if len(self) > int(self.__capacity * (2 / 3)):
            self.__resize()

    def __getitem__(self, key: Hashable) -> Any:
        hash_index = self.__index_to_read(key)
        return self._hash_table[hash_index].value

    def __len__(self) -> int:
        return self.__size

    def __delitem__(self, key: Hashable) -> None:
        hash_index = self.__index_to_read(key)
        self._hash_table[hash_index] = None
        self.__size -= 1

    def __repr__(self) -> str:
        str_ = "{"
        for el in self:
            str_ += f"'{el}': {self.get(el)}, "
        return str_[:-2] + "}"

    def __iter__(self) -> Iterator:
        list_ = []
        for i in range(self.__capacity):
            if self._hash_table[i] is not None:
                list_.append(self._hash_table[i].key)
        return iter(list_)

    def get(self, key: Hashable, default_value: Any = None) -> Any:
        try:
            item = self[key]
            return item
        except KeyError:
            return default_value

    def pop(self, key: Hashable, *default_value: Any) -> Any:
        if len(default_value) > 1:
            raise TypeError("Expected at most two argument")
        try:
            hash_index = self.__index_to_read(key)
            value = self._hash_table[hash_index]
            self.__delitem__(key)
            self.__size -= 1
            return value
        except KeyError:
            try:
                value = default_value[0]
                return value
            except IndexError:
                raise

    def update(self, other: dict | Dictionary) -> None:
        for key in other:
            self[key] = other.get(key)

    def clear(self) -> None:
        self.__size = 0
        self._hash_table = [None] * self.__capacity

    def __index_to_write(self, key: Hashable) -> int:
        hash_index = hash(key) % self.__capacity
        for i in range(hash_index, self.__capacity + hash_index):
            index = i % self.__capacity
            if (self._hash_table[index] is None
                    or self._hash_table[index].key == key
                    and self._hash_table[index].hash == hash(key)):
                return index

    def __index_to_read(self, key: Hashable) -> int:
        hash_index = hash(key) % self.__capacity
        for i in range(hash_index, self.__capacity + hash_index):
            index = i % self.__capacity
            if (self._hash_table[index] is not None
                    and self._hash_table[index].key == key
                    and self._hash_table[index].hash == hash(key)):
                return index
        raise KeyError

    def __resize(self) -> None:
        old_hash_table = self._hash_table
        self.__capacity *= 2
        self._hash_table = [None] * self.__capacity
        self.__size = 0
        for node in old_hash_table:
            if node is not None:
                self[node.key] = node.value
