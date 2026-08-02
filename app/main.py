from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.hash_table: list = [None] * 8

    def __len__(self) -> int:
        return self.length

    def __setitem__(self, key: Any, value: Any) -> None:
        hash_key = hash(key)
        index_key = hash_key % len(self.hash_table)
        while self.hash_table[index_key] is not None:
            if self.hash_table[index_key][0] == key:
                self.hash_table[index_key] = (key, hash_key, value)
                return
            else:
                index_key = (index_key + 1) % len(self.hash_table)
        self.hash_table[index_key] = (key, hash_key, value)
        self.length += 1
        if self.length / len(self.hash_table) > 2 / 3:
            self.resize()

    def resize(self) -> None:
        new_hash_table = [None] * (len(self.hash_table) * 2)
        for cell in self.hash_table:
            if cell is not None:
                new_index = cell[1] % len(new_hash_table)
                while new_hash_table[new_index] is not None:
                    new_index = (new_index + 1) % len(new_hash_table)
                new_hash_table[new_index] = cell
        self.hash_table = new_hash_table

    def __getitem__(self, key: Any) -> Any:
        hash_key = hash(key)
        index_key = hash_key % len(self.hash_table)
        while self.hash_table[index_key] is not None:
            if self.hash_table[index_key][0] != key:
                index_key = (index_key + 1) % len(self.hash_table)
            else:
                return self.hash_table[index_key][2]
        raise KeyError
