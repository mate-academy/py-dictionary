import copy
from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.load_factor = 8
        self.hash_table: list = [None] * self.load_factor

    def resize_hash_table(self) -> None:
        outdated_table = copy.copy(self.hash_table)
        self.load_factor *= 2
        self.hash_table = [None] * self.load_factor
        for item in outdated_table:
            if item:
                hash_place = item[1] % self.load_factor
                if not self.hash_table[hash_place]:
                    self.hash_table[hash_place] = item
                elif self.hash_table[hash_place]:
                    while True:
                        hash_place = (hash_place + 1) % self.load_factor
                        if not self.hash_table[hash_place]:
                            break
                    self.hash_table[hash_place] = item

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if isinstance(key, (list, dict, set)):
            raise TypeError("key must be of immutable type")
        hash_place = hash(key) % self.load_factor
        if not self.hash_table[hash_place]:
            self.hash_table[hash_place] = [key, hash(key), value]
            self.length += 1
        elif self.hash_table[hash_place]:
            while True:
                if (self.hash_table[hash_place]
                        and key == self.hash_table[hash_place][0]):
                    self.hash_table[hash_place][2] = value
                    break
                hash_place = (hash_place + 1) % self.load_factor
                if not self.hash_table[hash_place]:
                    self.hash_table[hash_place] = [key, hash(key), value]
                    self.length += 1
                    break
        if self.length > self.load_factor * (2 / 3):
            self.resize_hash_table()

    def __getitem__(self, key: Hashable) -> Any:
        hash_place = hash(key) % self.load_factor
        if not self.hash_table[hash_place]:
            raise KeyError("no key with such name")
        if self.hash_table[hash_place][0] == key:
            return self.hash_table[hash_place][2]
        while True:
            hash_place = (hash_place + 1) % self.load_factor
            if not self.hash_table[hash_place]:
                raise KeyError("no key with such name")
            elif self.hash_table[hash_place][0] == key:
                break
        return self.hash_table[hash_place][2]

    def __delitem__(self, key: Hashable) -> None:
        hash_place = hash(key) % self.load_factor
        original_hash_place = hash_place
        while True:
            if self.hash_table[hash_place]:
                if self.hash_table[hash_place][0] == key:
                    break
            hash_place = (hash_place + 1) % self.load_factor
            if hash_place == original_hash_place:
                raise KeyError("no key with such name")
        self.hash_table[hash_place] = None
        self.length -= 1

    def __len__(self) -> int:
        return self.length
