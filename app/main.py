from dataclasses import dataclass  # Creación de clas diccionario
from typing import Any, Hashable, Iterator

INITIAL_CAPACITY = 8
LOAD_FACTOR = 2 / 3
RESIZE_MULTIPLIER = 2


@dataclass
class Node:
    key: Hashable
    key_hash: int
    value: Any


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.hash_table: list = [None] * INITIAL_CAPACITY

    @staticmethod
    def _find_slot(table: list, key: Hashable, key_hash: int) -> int:
        index = key_hash % len(table)

        while table[index] is not None:
            node = table[index]
            if node.key_hash == key_hash and node.key == key:
                break
            index = (index + 1) % len(table)

        return index

    def _resize(self) -> None:
        new_table: list = [None] * (len(self.hash_table) * RESIZE_MULTIPLIER)

        for node in self.hash_table:
            if node is not None:
                index = self._find_slot(new_table, node.key, node.key_hash)
                new_table[index] = node

        self.hash_table = new_table

    def __setitem__(self, key: Hashable, value: Any) -> None:
        key_hash = hash(key)
        index = self._find_slot(self.hash_table, key, key_hash)
        node = self.hash_table[index]

        if node is not None:
            node.value = value
            return

        self.hash_table[index] = Node(key, key_hash, value)
        self.length += 1

        if self.length > len(self.hash_table) * LOAD_FACTOR:
            self._resize()

    def __getitem__(self, key: Hashable) -> Any:
        index = self._find_slot(self.hash_table, key, hash(key))
        node = self.hash_table[index]

        if node is None:
            raise KeyError(f"Key {key!r} is not in the dictionary")

        return node.value

    def __len__(self) -> int:
        return self.length

    @staticmethod
    def _home_is_after_hole(home: int, hole: int, index: int) -> bool:
        if hole <= index:
            return hole < home <= index
        return home > hole or home <= index

    def __delitem__(self, key: Hashable) -> None:
        size = len(self.hash_table)
        hole = self._find_slot(self.hash_table, key, hash(key))

        if self.hash_table[hole] is None:
            raise KeyError(f"Key {key!r} is not in the dictionary")

        self.length -= 1
        index = hole

        while True:
            index = (index + 1) % size
            node = self.hash_table[index]

            if node is None:
                break

            home = node.key_hash % size
            if self._home_is_after_hole(home, hole, index):
                continue

            self.hash_table[hole] = node
            hole = index

        self.hash_table[hole] = None

    def get(self, key: Hashable, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: Hashable) -> Any:
        value = self[key]
        del self[key]
        return value

    def clear(self) -> None:
        self.length = 0
        self.hash_table = [None] * INITIAL_CAPACITY

    def __iter__(self) -> Iterator[Hashable]:
        for node in self.hash_table:
            if node is not None:
                yield node.key

    def update(self, other: "Dictionary") -> None:
        for key in other:
            self[key] = other[key]
