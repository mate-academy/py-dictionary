from __future__ import annotations
from typing import Any, Union


class Dictionary:
    THRESHOLD = 2 / 3

    def __init__(self) -> None:
        self.hash_table: list = [None] * 8
        self.capacity = 8
        self.length = 0

    def __repr__(self) -> str:
        return f"{list(filter(lambda x: x is not None, self.hash_table))}"

    def __setitem__(self,
                    key: Union[str, int, tuple, bool, float],
                    value: Any) -> None:

        if len(self) == int(self.capacity * self.THRESHOLD):
            self.__size_increase()

        item_hash = hash(key)
        item_index = item_hash % self.capacity

        if key in self.keys():
            while (self.hash_table[item_index] is not None
                   and self.hash_table[item_index][0] != key):
                if item_index == self.capacity - 1:
                    item_index = 0
                else:
                    item_index += 1

            self.hash_table[item_index][1] = value
            return

        if self.hash_table[item_index]:
            while self.hash_table[item_index] is not None:
                if item_index == self.capacity - 1:
                    item_index = 0
                else:
                    item_index += 1

        self.hash_table[item_index] = [key, value]
        self.length += 1

    def __getitem__(self,
                    key: Union[str, int, tuple, bool, float]) -> Any:

        if key not in self.keys():
            raise KeyError

        item_hash = hash(key)
        item_index = item_hash % self.capacity

        if self.hash_table[item_index][0] == key:
            return self.hash_table[item_index][1]

        while self.hash_table[item_index][0] != key:
            if item_index == self.capacity - 1:
                item_index = 0
            else:
                item_index += 1

        return self.hash_table[item_index][1]

    def __delitem__(self,
                    key: Union[str, int, tuple, bool, float]) -> None:

        if key not in self.keys():
            raise KeyError

        item_hash = hash(key)
        item_index = item_hash % self.capacity

        while (self.hash_table[item_index] is not None
               and self.hash_table[item_index][0] != key):
            if item_index == self.capacity - 1:
                item_index = 0
            else:
                item_index += 1

        self.hash_table[item_index] = None
        self.length -= 1

    def __len__(self) -> int:
        return self.length

    def __iter__(self) -> Dictionary:
        self.clear_table = list(
            filter(lambda x: x is not None, self.hash_table)
        )
        self.index = 0
        return self

    def __next__(self) -> list:
        if self.index == len(self.clear_table):
            raise StopIteration
        return_value = self.clear_table[self.index]
        self.index += 1
        return return_value

    def __size_increase(self) -> None:
        old_table = self.hash_table.copy()

        self.capacity *= 2
        self.hash_table = [None] * self.capacity
        self.length = 0

        for item in old_table:
            if item:
                key, value = item
                self.__setitem__(key, value)

    def keys(self) -> list:
        _keys = []

        for item in self.hash_table:
            if item is not None:
                _keys.append(item[0])

        return _keys

    def values(self) -> list:
        _values = []

        for item in self.hash_table:
            if item is not None:
                _values.append(item[1])

        return _values

    def clear(self) -> None:
        self.hash_table = [None] * 8
        self.length = 0

    def get(self,
            key: Union[str, int, tuple, bool, float]) -> Any:

        return self.__getitem__(key)

    def update(self, update: dict) -> None:
        for key, value in update.items():
            self.__setitem__(key, value)

    def pop(self,
            key: Union[str, int, tuple, bool, float]) -> Any:

        return_value = self.__getitem__(key)
        self.__delitem__(key)
        return return_value
