from __future__ import annotations
from typing import Any, Hashable


class Dictionary:
    size = 0

    def __init__(
            self,
            capacity: int = 8,
            load_factor_threshold: float = 0.6
    ) -> None:
        self._capacity = capacity
        self._hash_table = capacity * [None]
        self._load_factor_threshold = load_factor_threshold

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.size / self._capacity >= self._load_factor_threshold:
            self.resize_and_rehash()
        index = self._index(key)
        while self._hash_table[index]:
            if self._hash_table[index][1] == key:
                self._hash_table[index][2] = value
                return
            else:
                index = (index + 1) % self._capacity
        self._hash_table[index] = [hash(key), key, value]
        self.size += 1

    def __getitem__(self, key: Hashable) -> Any:
        index = self._index(key)
        while self._hash_table[index]:
            if self._hash_table[index][1] == key:
                return self._hash_table[index][2]
            index = (index + 1) % self._capacity
        raise KeyError

    def __len__(self) -> int:
        return self.size

    def _index(self, key: Hashable) -> int:
        return hash(key) % self._capacity

    def resize_and_rehash(self) -> None:
        old_hash_table = self._hash_table
        self._capacity *= 2
        self._hash_table = self._capacity * [None]
        self.size = 0

        for el in old_hash_table:
            if el:
                index = self._index(el[1])
                while self._hash_table[index]:
                    if self._hash_table[index][1] == el[1]:
                        self._hash_table[index][2] = el[2]
                        return
                    else:
                        index = (index + 1) % self._capacity
                self._hash_table[index] = [hash(el[1]), el[1], el[2]]
                self.size += 1

    def __eq__(self, other: Dictionary) -> bool:
        print(f"self: {self}, other: {other}")
        if self is other:
            return True
        if type(self) is not type(other):
            return False
