from collections.abc import Hashable
from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.capacity = 8
        self.load_factor = 2 / 3
        self.hash_table: list = [None] * self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.length == round(self.capacity * self.load_factor):
            self.resize()
        table_index = hash(key) % self.capacity
        if self.hash_table[table_index] is None:
            self.hash_table[table_index] = []
        for cell in self.hash_table[table_index]:
            if cell[0] == key and cell[1] == hash(key):
                cell[2] = value
                return

        self.hash_table[table_index].append([key, hash(key), value])
        self.length += 1

    def __getitem__(self, item: Hashable) -> Any:
        table_index = hash(item) % self.capacity
        if self.hash_table[table_index] is None:
            raise KeyError
        for cell in self.hash_table[table_index]:
            if cell[0] == item and cell[1] == hash(item):
                return cell[2]
        raise KeyError

    def __len__(self) -> int:
        return self.length

    def resize(self) -> None:
        self.capacity *= 2
        old_table_copy = self.hash_table.copy()
        self.hash_table = [None] * self.capacity
        self.length = 0
        for cell in old_table_copy:
            if cell is None:
                continue
            for ele in cell:
                self[ele[0]] = ele[2]
