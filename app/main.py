from __future__ import annotations
from typing import Hashable, Any


class Dictionary:
    def __init__(self, **kwargs) -> None:
        self._capacity = 8
        self._length = 0
        self._load_factor = 2 / 3
        self._threshold = int(self._capacity * self._load_factor)
        self._hash_table = [[]] * self._capacity

        for key, value in kwargs.items():
            self[key] = value

    def __setitem__(self, key: Hashable, value: Any) -> None:
        hash_key = hash(key)
        key_hash_value = [key, hash_key, value]
        index = hash_key % self._capacity

        while True:
            if not self._hash_table[index]:
                self._hash_table[index] = key_hash_value
                self._length += 1
                break
            if self._hash_table[index][:2] == key_hash_value[:2]:
                self._hash_table[index][2] = value
                break
            index = (index + 1) % self._capacity

        if self._length > self._threshold:
            self._resize_array()

    def __getitem__(self, key: Hashable) -> Any:
        hash_key = hash(key)
        index = hash_key % self._capacity

        while self._hash_table[index]:
            if self._hash_table[index][:2] == [key, hash_key]:
                return self._hash_table[index][2]
            index = (index + 1) % self._capacity

        raise KeyError

    def __len__(self) -> int:
        return self._length

    def _resize_array(self) -> None:
        self._capacity *= 2
        self._length = 0
        self._threshold = int(self._capacity * self._load_factor)

        old_table = self._hash_table
        self._hash_table = [[]] * self._capacity

        for key_hash_value in old_table:
            if key_hash_value:
                self.__setitem__(key_hash_value[0], key_hash_value[2])
