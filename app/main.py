import copy

from typing import Any
from app.point import Point


class Dictionary:

    def __init__(self) -> None:
        self.current_capacity = 8
        self.hash_table: list = [None] * self.current_capacity
        self.threshold = int(self.current_capacity * 2 / 3)
        self.size: int = 0

    def _get_target_ceil_index(self, index_current: int, key: Any) -> int:  # TO DO correct types annotation, replace any.
        index_current = (index_current + 1) % self.current_capacity  # linear billing
        while (self.hash_table[index_current] is not None
               and self.hash_table[index_current][0] != key):
            index_current = (index_current + 1) % self.current_capacity
        return index_current

    def _resize(self, new_key, new_value, hash_key) -> None:  # TO DO ARGS ACTUAL KEY ...

        temporary_obj = copy.copy(self.hash_table)
        self.current_capacity *= 2
        self.hash_table = [None] * self.current_capacity
        self.threshold = int(self.current_capacity * 2 / 3)
        self.size = 0

        for item in temporary_obj:  # 1) what will happen withe temporary obj?
            if item is not None:
                old_key, old_value, old_hash_key = item
                self._write_into_dict(
                    old_key,
                    old_value,
                    old_hash_key
                )
        self._write_into_dict(new_key, new_value, hash_key)

    def _write_into_dict(self, *args) -> None:
        key, value, hash_key = args  # hash key get in __set_item__

        index_current = int(hash_key % self.current_capacity)

        if self.hash_table[index_current] is None:  # if after hashing we get free ceil we will write item there.
            if self.size < self.threshold:  # checks the size before writing
                self.hash_table[index_current] = [
                    key,
                    value,
                    hash_key
                ]
                self.size += 1
            elif self.size == self.threshold:  # if size == threshold we make resize the table
                self._resize(key, value, hash_key)
        elif self.hash_table[index_current][0] == key:  # if we get the ceil ...
            # with the same key we will write it item instead existed item.
            self.hash_table[index_current] = [
                key,
                value,
                hash_key
            ]
        elif self.hash_table[index_current][0] != key:  # if in the same key we found not the same key we should find
            index_current = self._get_target_ceil_index(index_current, key)

            if self.hash_table[index_current] is None:
                if self.size < self.threshold:
                    self.hash_table[index_current] = [
                        key,
                        value,
                        hash_key
                    ]
                    self.size += 1
                elif self.size == self.threshold:
                    self._resize(key, value, hash_key)
            elif self.hash_table[index_current][0] == key:
                self.hash_table[index_current] = [
                    key,
                    value,
                    hash_key
                ]

    def __setitem__(self, key, value) -> None:
        if isinstance(key, (dict, set, list)):  # check if the key not unhashable type
            raise TypeError(f"{key}: object is not subscriptable")

        hash_key = hash(key)  # if current key is hashable we get hash

        self._write_into_dict(key, value, hash_key)  # put taken: key, value and hash_key into func for writing

    def __getitem__(self, item) -> Any:

        if isinstance(item, (dict, set, list)):  # we check the type of the object
            raise KeyError(f"{item}: unhashable type")

        hash_key = hash(item)
        index_current = int(hash_key % self.current_capacity)

        if self.hash_table[index_current] is None:
            raise KeyError(f"{item}")
        elif self.hash_table[index_current][0] == item:
            return self.hash_table[index_current][1]
        elif self.hash_table[index_current][0] != item:
            index_current = self._get_target_ceil_index(index_current, item)

            if self.hash_table[index_current] is None:
                raise KeyError(f"{item}")
            elif self.hash_table[index_current][0] == item:
                return self.hash_table[index_current][1]

    def __len__(self) -> int:
        return self.size
