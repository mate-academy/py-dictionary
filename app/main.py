from __future__ import annotations

from typing import Iterable
from typing import Hashable, Any


INITIAL_CAPACITY = 8
RESIZE_THRESHOLD = 0.66
CAPACITY_MULTIPLIER = 2


class Dictionary:
    def __init__(self) -> None:
        self.capacity = INITIAL_CAPACITY
        self.size = 0
        self._load_factor_calculation()
        self._list_creation()

    def _resize(self) -> None:
        temp_data = self.data
        self.capacity *= CAPACITY_MULTIPLIER
        self._load_factor_calculation()
        self._list_creation()
        self.size = 0
        for element in temp_data:
            if element:
                self.__setitem__(element[0], element[-1])

    def _load_factor_calculation(self) -> None:
        self.load_factor = round(self.capacity * RESIZE_THRESHOLD)

    def _list_creation(self) -> None:
        self.data = [None for _ in range(self.capacity)]

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.size == self.load_factor:
            self._resize()
        if not self.data:
            self._list_creation()

        hash_key = hash(key)
        index = hash_key % self.capacity
        while True:
            if index == self.capacity:
                index = 0
            if self.data[index] is None:
                self.data[index] = (key, hash_key, value)
                self.size += 1
                break
            elif self.data[index][0] == key:
                self.data[index] = (key, hash_key, value)
                break
            index += 1

    def __getitem__(self, key: Hashable) -> Any:
        hash_key = hash(key)
        index = hash_key % self.capacity
        if self.data[index] is None:
            raise KeyError(
                "Dictionary doesn't have any value with provided key!"
            )

        for element in self.data:
            if element is None:
                continue
            elif element[0] == key:
                return element[-1]

    def get(self, key: Hashable, default: Any = None) -> Any:
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def __len__(self) -> int:
        return self.size

    def pop(self, key: Hashable, default: Any = None) -> Any:
        if self.get(key):
            for index, item in enumerate(self.data):
                if item is None:
                    continue
                elif item[0] == key:
                    pop_item = self.get(key)
                    self.__delitem__(key)
                    return pop_item
        elif default is None:
            raise KeyError(
                "Key is not found and default argument wasn't provided"
            )
        return default

    def __delitem__(self, key: Hashable) -> None:
        for index, item in enumerate(self.data):
            if item is None:
                continue
            elif item[0] == key:
                self.data[index] = None
                self.size -= 1
                return
        raise KeyError("Dictionary doesn't have any value with provided key!")

    def update(self, iterable: Iterable) -> None:
        for element in iterable:
            self.__setitem__(element[0], element[-1])

    def __iter__(self) -> Dictionary:
        self.index = -1
        return self

    def __next__(self) -> tuple:
        self.index += 1
        if self.index >= len(self.data):
            raise StopIteration
        return self.data[self.index]

    def clear(self) -> None:
        self.capacity = 8
        self.size = 0
        self._load_factor_calculation()
        self._list_creation()
