from __future__ import annotations
from typing import Any, Hashable, Optional


class CustomDummyValue:
    def __init__(self, key_name: Hashable) -> None:
        self.key_name = key_name


class Dictionary:
    LOAD_FACTOR = 2 / 3
    RESIZE_COEFFICIENT = 2
    DUMMY_VALUE = CustomDummyValue

    class DictionaryIterator:
        def __init__(self, hash_table: list) -> None:
            self.counter = 0
            self.hash_table = hash_table

        def __iter__(self) -> Dictionary.DictionaryIterator:
            self.counter = 0
            return self

        def __next__(self) -> Any:

            try:
                while True:
                    if self.hash_table[self.counter]:
                        result = self.hash_table[self.counter][0]
                        self.counter += 1
                        return result
                    self.counter += 1
            except IndexError:
                raise StopIteration

    def __init__(self) -> None:
        self.length = 0
        self.capacity = 8
        self.threshold = self.capacity * self.LOAD_FACTOR
        self.hash_table: list = [None] * self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:

        key_hash = hash(key)
        key_index = self._get_index_hash_table(
            key,
            key_hash
        )
        if not self.hash_table[key_index]:
            self.length += 1

        self.hash_table[key_index] = (
            key, key_hash, value
        )

        if self.length >= self.threshold:
            self._resize()

    def __getitem__(self, key: Hashable) -> Any:
        key_hash = hash(key)
        key_index = self._get_index_hash_table(
            key, key_hash
        )
        if self.hash_table[key_index] is None:
            raise KeyError(key)

        return self.hash_table[key_index][2]

    def __len__(self) -> int:
        return self.length

    def __delitem__(self, key: Hashable) -> None:
        key_hash = hash(key)

        key_index = self._get_index_hash_table(
            key, key_hash
        )

        if self.hash_table[key_index][0] is self.DUMMY_VALUE:
            raise KeyError(key)

        self.hash_table[key_index] = (
            self.DUMMY_VALUE(key), None, None
        )

    def __iter__(self) -> DictionaryIterator:
        return self.DictionaryIterator(self.hash_table)

    def _get_index_hash_table(
            self,
            key: Hashable,
            key_hash: int,
            capacity: int = None,
            hash_table: list = None
    ) -> int:

        if not capacity:
            capacity = self.capacity

        if not hash_table:
            hash_table = self.hash_table

        key_index = key_hash % capacity

        while hash_table[key_index] is not None:
            hash_table_key = hash_table[key_index][0]
            if isinstance(hash_table_key, self.DUMMY_VALUE):
                if hash_table_key.key_name == key:
                    break

            if all(
                    [hash_table_key == key,
                     isinstance(hash_table_key, type(key))]
            ):
                break
            key_index = (key_index + 1) % capacity

        return key_index

    def _resize(self) -> None:
        capacity = self.capacity * self.RESIZE_COEFFICIENT

        resize_hash_table = [None] * capacity

        self.length = 0
        for data in self.hash_table:
            if data is not None:
                new_index = self._get_index_hash_table(
                    key=data[0],
                    key_hash=data[1],
                    capacity=capacity,
                    hash_table=resize_hash_table
                )

                resize_hash_table[new_index] = data
                self.length += 1

        self.hash_table = resize_hash_table
        self.threshold = int(capacity * self.LOAD_FACTOR)
        self.capacity = capacity

    def clear(self) -> None:
        self.length = 0
        self.capacity = 8
        self.threshold = self.capacity * self.LOAD_FACTOR
        self.hash_table: list = [None] * self.capacity

    def get(
            self,
            key: Hashable,
            default_value: Optional[Any] = None
    ) -> Optional[Any]:
        try:
            return self.__getitem__(key)
        except KeyError:
            return default_value

    def update(self, custom_dict: Dictionary) -> None:
        if not isinstance(custom_dict, self.__class__):
            raise ValueError(f"custom_dict must be instance {self.__class__}")
        for key in custom_dict:
            self[key] = custom_dict[key]
