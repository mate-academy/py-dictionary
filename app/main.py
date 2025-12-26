import math
from typing import Any, Hashable

LOAD_FACTOR = 2 / 3


class Dictionary:

    def __init__(self) -> None:
        self._initialize_hash_table(8)
        self.data = []
        self.capacity = 0

    def __setitem__(self, key: Hashable, value: Any) -> None:
        self.data.append([key, value])
        self.create_hash_table(key, value)
        self.capacity += 1
        if self.capacity >= math.floor(len(self.hash_table) * LOAD_FACTOR):
            self._resize()

    def __getitem__(self, key_: Hashable) -> Any:
        for key, value in self.data:
            if key == key_:
                return value
        raise KeyError(f"Key '{key_}' not found in the dictionary")

    def __len__(self) -> int:
        return len(self.data)

    def _initialize_hash_table(self, hash_table_len: int) -> None:
        self.hash_table = [[key, None] for key in range(hash_table_len)]

    def create_hash_table(self, key: Hashable, value: Any) -> None:
        cell_index = hash(key) % len(self.hash_table)
        while True:
            if self.hash_table[cell_index][1]:
                if self.hash_table[cell_index][1][0] == key:
                    for data in self.data:
                        if data[0] == key:
                            self.data.remove(data)
                            break
                    self.hash_table[cell_index][1] = [key, hash(key), value]
                    self.capacity -= 1
                    break
                cell_index = (cell_index + 1) % len(self.hash_table)
            if self.hash_table[cell_index][1] is None:
                self.hash_table[cell_index][1] = [key, hash(key), value]
                break

    def _resize(self) -> None:
        copy_hash_table = self.hash_table.copy()
        size_table = len(self.hash_table) * 2
        self._initialize_hash_table(size_table)
        for stored_node in copy_hash_table:
            if stored_node[1] is not None:
                key = stored_node[1][0]
                value = stored_node[1][2]
                self.create_hash_table(key, value)
