from collections import namedtuple
from typing import Any

Node = namedtuple("Node", ["key", "hash_value", "value"])


class Dictionary:
    def __init__(self) -> None:
        self.hash_table: list = [None] * 8
        self.length = 0
        self.load_factor = 0.75

    def __len__(self) -> int:
        return self.length

    def _find_index(self, key: Any) -> int:
        index = hash(key) % len(self.hash_table)

        for _ in range(len(self.hash_table)):
            cell = self.hash_table[index]

            if cell is None:
                return index
            elif cell.hash_value == hash(key) and cell.key == key:
                return index
            else:
                index = (index + 1) % len(self.hash_table)

        raise RuntimeError("hash table is full, resize failed")

    def __setitem__(self, key: Any, value: Any) -> None:
        current_load_factor = self.length / len(self.hash_table)

        if current_load_factor >= self.load_factor:
            self._resize()
        index = self._find_index(key)

        if self.hash_table[index] is None:
            self.length += 1

        self.hash_table[index] = Node(key, hash(key), value)

    def __getitem__(self, key: Any) -> Any:
        index = self._find_index(key)

        if self.hash_table[index] is None:
            raise KeyError(f"Key {key} doesn't exist!")

        return self.hash_table[index].value

    def _resize(self) -> None:
        old_hash_table = self.hash_table

        self.hash_table = [None] * (len(old_hash_table) * 2)

        for cell in old_hash_table:
            if cell is not None:
                index = self._find_index(cell.key)
                self.hash_table[index] = cell
