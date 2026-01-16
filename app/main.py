from __future__ import annotations
from typing import Hashable, Any, TypeAlias


Key: TypeAlias = Hashable
Value: TypeAlias = Any


class Dictionary:

    _hash_table_node = [None, None, None]  # [hash, key, value]

    def __init__(self) -> None:
        self._hash_table = [self._hash_table_node for _ in range(8)]

    def __str__(self) -> str:
        return self._normalized_table().__str__()

    def __setitem__(
            self,
            key: Hashable,
            value: Any
    ) -> None:
        if self.__len__() == int(len(self._hash_table) * (2 / 3)):
            self._resize_hash_table()

        _index = hash(key) % len(self._hash_table)

        while self._hash_table[_index] != self._hash_table_node:
            if key == self._hash_table[_index][1]:
                break
            _index += 1
            if _index == len(self._hash_table):
                _index = 0

        self._hash_table[_index] = [hash(key), key, value]

    def __getitem__(self, key: Any) -> Any:

        return self._hash_table[self._find_index(key)][2]

    def __len__(self) -> int:
        return len(
            self._normalized_table()
        )

    def __delitem__(self, key: Hashable) -> None:
        index = self._find_index(key)
        self._hash_table[index] = self._hash_table_node

    def __iter__(self) -> Dictionary:
        self._counter = 0
        return self

    def __next__(self) -> list:
        if self._counter < len(self._normalized_table()):
            _node = self._normalized_table()[self._counter]
            self._counter += 1
            return _node

        raise StopIteration

    def _find_index(self, key: Any) -> int:
        _index = _start_index = hash(key) % len(self._hash_table)

        while True:
            if self._hash_table[_index][1] == key:
                return _index
            _index += 1
            if _index >= len(self._hash_table):
                _index = 0
            if _index == _start_index:
                break
        raise KeyError(f"Key {key} not found.")

    def _resize_hash_table(self) -> None:
        self._hash_table_copy = self._hash_table
        self._hash_table = ([self._hash_table_node]
                            * (len(self._hash_table) * 2))
        for node in self._hash_table_copy:
            if node != self._hash_table_node:
                self.__setitem__(node[1], node[2])

    def _normalized_table(self) -> list:
        return [
            [node[1], node[2]] for node in self._hash_table
            if node != self._hash_table_node
        ]

    def clear(self) -> None:
        self.__init__()

    def get(
            self,
            key: Any,
            returned_value_if_key_not_found: Any = None
    ) -> Any:
        try:
            return self.__getitem__(key)
        except KeyError:
            return returned_value_if_key_not_found

    def pop(self, index: int) -> None:
        _node = self._normalized_table()[index]
        self.__delitem__(_node[0])
        return _node

    def update(self, new_items: list[(Key, Value)]) -> None:
        for new_item in new_items:
            self.__setitem__(new_item[0], new_item[1])
