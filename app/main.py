from dataclasses import dataclass
from typing import Hashable, Any


@dataclass
class Node:
    hash_: int
    key: Hashable
    value: Any


class Dictionary:
    def __init__(self) -> None:
        self._capacity = 8
        self._factor = 2 / 3
        self._size = 0
        self._hash_table: list[Node | None] = [None] * self._capacity

    def __len__(self) -> int:
        return self._size

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self._factor_is_reached():
            self._resize()
        self._add_pair_to_hash_table(key, value)

    def __getitem__(self, key: Hashable) -> Any:
        index = self._find_index(key)
        if self._is_cell_empty(index):
            raise KeyError(f"Key {key} is not present in the hash table")
        return self._hash_table[index].value

    def _find_index(self, key: Hashable) -> int:
        hash_ = hash(key)
        index = hash_ % self._capacity

        while (self._hash_table[index] is not None
               and (self._hash_table[index].hash_ != hash_
                    or self._hash_table[index].key != key)):
            index += 1
            index %= self._capacity

        return index

    def _resize(self) -> None:
        old_hash_table = self._hash_table
        self._capacity *= 2
        self._hash_table = [None] * self._capacity
        self._size = 0

        for item in old_hash_table:
            if item is not None:
                self[item.key] = item.value

    def _factor_is_reached(self) -> bool:
        return self._size >= self._capacity * self._factor

    def _is_cell_empty(self, cell_index: int) -> bool:
        return self._hash_table[cell_index] is None

    def _add_pair_to_hash_table(self, key: Hashable, value: Any) -> None:
        index = self._find_index(key)

        if self._is_cell_empty(index):
            self._size += 1

        self._hash_table[index] = Node(hash(key), key, value)
