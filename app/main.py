from __future__ import annotations
from typing import Any, Hashable, Iterator


class Node:
    def __init__(self, key: Hashable, value: Any) -> None:
        self.key = key
        self.value = value
        self.removed = False

    def __repr__(self) -> str:
        return f"{self.key} : {self.value}"


class Dictionary:
    _THRESHOLD = 0.66
    _DEFAULT_CAPACITY = 8

    def __init__(self) -> None:
        self._capacity = Dictionary._DEFAULT_CAPACITY
        self._data = self._make_blank()
        self._size = 0

    def __repr__(self) -> str:
        return f"Dictionary({self._data})"

    def _make_blank(self) -> list:
        return [None] * self._capacity

    def __len__(self) -> int:
        return self._size

    def _get_index(self, key: Hashable) -> int:
        return hash(key) % self._capacity

    def _resize(self) -> None:
        old_data = self._data
        self._capacity *= 2
        self._data = self._make_blank()
        self._size = 0
        for node in old_data:
            if node:
                self.__setitem__(node.key, node.value)
        del old_data

    def __getitem__(self, key: Hashable) -> Any:
        cur_index = self._get_index(key)
        while (
            self._data[cur_index] is not None
            and (self._data[cur_index].removed
                 or self._data[cur_index].key != key)
        ):
            cur_index = (cur_index + 1) % self._capacity
        if self._data[cur_index] is None:
            raise KeyError
        return self._data[cur_index].value

    def __setitem__(self, key: Hashable, value: Any) -> Any:
        if self._size + 1 > self._capacity * Dictionary._THRESHOLD:
            self._resize()
        new_node = Node(key, value)
        cur_index = self._get_index(key)
        while (
            self._data[cur_index] is not None
            and not self._data[cur_index].removed
        ):
            if self._data[cur_index].key == key:
                self._data[cur_index] = new_node
                return
            cur_index = (cur_index + 1) % self._capacity
        self._data[cur_index] = new_node
        self._size += 1

    def clear(self) -> None:
        self._capacity = Dictionary._DEFAULT_CAPACITY
        self._data = self._make_blank()
        self._size = 0

    def __delitem__(self, key: Hashable) -> None:
        cur_index = self._get_index(key)
        while (
            self._data[cur_index] is not None
            and (self._data[cur_index].removed
                 or self._data[cur_index].key != key)
        ):
            cur_index = (cur_index + 1) % self._capacity
        if self._data[cur_index] is None:
            raise KeyError
        self._data[cur_index].removed = True
        self._size -= 1

    def get(self, key: Hashable, default: Any = None) -> Any:
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def update(self, other: Dictionary | dict) -> None:
        if isinstance(other, Dictionary | dict):
            for key in other:
                self.__setitem__(key, other[key])

    def __iter__(self) -> Iterator:
        self._ind = 0
        return self

    def __next__(self) -> Any:
        while (
            self._ind < self._capacity
            and (self._data[self._ind] is None
                 or self._data[self._ind].removed)
        ):
            self._ind += 1
        if self._ind == self._capacity:
            raise StopIteration
        result = self._data[self._ind].key
        self._ind += 1
        return result
