import copy

from typing import Any


class Dictionary:

    def __init__(self) -> None:
        self.current_capacity = 8
        self.hash_table: list = [None] * self.current_capacity
        self.threshold = int(self.current_capacity * 2 / 3)
        self.length: int = 0

    def _get_target_ceil_index(
            self,
            index_current: int,
            key: int | float | tuple | str | object
    ) -> int:
        index_current = (index_current + 1) % self.current_capacity
        while (self.hash_table[index_current] is not None
               and self.hash_table[index_current][0] != key):
            index_current = (index_current + 1) % self.current_capacity
        return index_current

    def _resize(
            self,
            new_key: int | float | tuple | str | object,
            new_value: Any,
            hash_key: int
    ) -> None:

        temporary_obj = copy.copy(self.hash_table)
        self.current_capacity *= 2
        self.hash_table = [None] * self.current_capacity
        self.threshold = int(self.current_capacity * 2 / 3)
        self.length = 0

        for item in temporary_obj:
            if item is not None:
                old_key, old_value, old_hash_key = item
                self._write_into_dict(
                    old_key,
                    old_value,
                    old_hash_key
                )
        self._write_into_dict(new_key, new_value, hash_key)

    def _write_into_dict(self, *args) -> None:
        key, value, hash_key = args

        index_current = int(hash_key % self.current_capacity)

        if self.hash_table[index_current] is None:
            if self.length < self.threshold:
                self.hash_table[index_current] = [
                    key,
                    value,
                    hash_key
                ]
                self.length += 1
            elif self.length == self.threshold:
                self._resize(key, value, hash_key)
        elif self.hash_table[index_current][0] == key:
            self.hash_table[index_current] = [
                key,
                value,
                hash_key
            ]
        elif self.hash_table[index_current][0] != key:
            index_current = self._get_target_ceil_index(index_current, key)

            if self.hash_table[index_current] is None:
                if self.length < self.threshold:
                    self.hash_table[index_current] = [
                        key,
                        value,
                        hash_key
                    ]
                    self.length += 1
                elif self.length == self.threshold:
                    self._resize(key, value, hash_key)
            elif self.hash_table[index_current][0] == key:
                self.hash_table[index_current] = [
                    key,
                    value,
                    hash_key
                ]

    def __setitem__(self,
                    key: int | float | tuple | str | object,
                    value: Any
                    ) -> None:
        if isinstance(key, (dict, set, list)):
            raise TypeError(f"{key}: object is not subscriptable")

        hash_key = hash(key)
        self._write_into_dict(key, value, hash_key)

    def __getitem__(self, item: int | float | tuple | str | object) -> Any:
        if isinstance(item, (dict, set, list)):
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
        return self.length
