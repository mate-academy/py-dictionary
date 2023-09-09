from __future__ import annotations
from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.hash_table: list = [None] * 8
        self.keys: list = []

    def __len__(self) -> int:
        return self.length

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = hash(key) % len(self.hash_table)

        if not self.hash_table[index]:
            self.hash_table[index] = (key, hash(key), value)
            self.length += 1
            self.keys.append(key)
        elif (
                self.hash_table[index][0] == key
                and hash(key) == self.hash_table[index][1]
        ):
            self.hash_table[index] = (key, hash(key), value)
        elif key in self.keys:
            for cell_number in range(index + 1, len(self.hash_table) + index):
                if cell_number >= len(self.hash_table):
                    cell_number % len(self.hash_table)
                if (
                        self.hash_table[cell_number][0] == key
                        and self.hash_table[cell_number][1] == hash(key)
                ):
                    self.hash_table[cell_number] = (key, hash(key), value)
                    break
        else:
            index = self.find_empty_place(index)
            self.hash_table[index] = (key, hash(key), value)
            self.length += 1
            self.keys.append(key)

        if self.length > len(self.hash_table) * 2 / 3:
            self.resize()

    def __getitem__(self, key: Hashable) -> Any:
        capacity = len(self.hash_table)
        index = hash(key) % capacity
        if (
                self.hash_table[index]
                and key == self.hash_table[index][0]
                and self.hash_table[index][1] == hash(key)
        ):
            return self.hash_table[index][2]
        for cell in range(index, capacity + index):
            if cell >= capacity:
                cell = cell % capacity
            if (
                self.hash_table[index]
                and key == self.hash_table[cell][0]
                and self.hash_table[cell][1] == hash(key)
            ):
                return self.hash_table[cell][2]
        raise KeyError

    def clear(self) -> None:
        self.__init__()

    def __delitem__(self, key: Hashable) -> None:
        if key in self.keys:
            index = hash(key) % len(self.hash_table)
            if (
                    self.hash_table[index] == key
                    and self.hash_table[index][1] == hash(key)
            ):
                self.hash_table[index] = None
            else:
                for cell in range(index + 1, len(self.hash_table) + index):
                    if cell >= len(self.hash_table):
                        cell %= len(self.hash_table)
                    if (
                        self.hash_table[cell]
                        and self.hash_table[cell][0] == key
                        and self.hash_table[cell][1] == hash(key)
                    ):
                        self.hash_table[cell] = None
            self.keys.remove(key)
            self.length -= 1

    def find_empty_place(self, current_index: int) -> int | None:
        capacity = len(self.hash_table)
        for index in range(current_index + 1, capacity + current_index):
            if index >= capacity:
                index %= capacity
            if not self.hash_table[index]:
                return index

    def resize(self) -> None:
        old_hash_table = self.hash_table
        self.hash_table = [None] * len(self.hash_table) * 2
        for cell in old_hash_table:
            if cell:
                index = cell[1] % len(self.hash_table)
                if not self.hash_table[index]:
                    self.hash_table[index] = cell
                else:
                    index = self.find_empty_place(index)
                    self.hash_table[index] = cell
