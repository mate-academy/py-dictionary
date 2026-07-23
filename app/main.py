import random

from typing import Any


class Dictionary:
    def __setitem__(self, key, value) -> None:
        cell = hash(key) % self.len_hash_table
        if self.hash_table[cell][0] is not None:
            if self.hash_table[cell][0] == key:
                self.hash_table[cell][1] = value
            else:
                self.__setitem__(random.choice([i for i in range(self.len_hash_table)]), value)
        else:
            self.hash_table[cell][0] = key
            self.hash_table[cell][1] = value

    def __getitem__(self, key) -> Any:
        return self.hash_table[
            hash(key) % self.len_hash_table
        ][1]

    def __len__(self) -> int:
        return all(all(i) for i in self.hash_table)

    def __init__(self) -> None:
        self.hash_table = [[None, None] for _ in range(8)]
        self.len_hash_table = 8
