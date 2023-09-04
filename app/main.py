from collections import namedtuple
from collections.abc import Hashable
from typing import Any


class Dictionary:
    LOAD_FACTOR: float = 2 / 3

    def __init__(self) -> None:
        self._capacity: int = 8
        self._length: int = 0
        self._Item = namedtuple("_Item", ["key", "hash", "value"])

        self._items: list = [None] * self._capacity

    def _resize_table(self) -> None:
        old_items: list = self._items
        self._capacity *= 2
        self._items = [None] * self._capacity
        self._length = 0
        for item in old_items:
            if item is not None:
                self.__setitem__(item.key, item.value)

    def _find_index(self, key: Hashable) -> int:
        element_index: int = hash(key) % self._capacity
        while self._items[element_index] is not None and (
            self._items[element_index].hash != hash(key)
            or self._items[element_index].key != key
        ):
            element_index = (element_index + 1) % self._capacity
        return element_index

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self._length >= int(self._capacity * self.LOAD_FACTOR):
            self._resize_table()

        element_index = self._find_index(key)
        new_item = self._Item(key, hash(key), value)
        if self._items[element_index] is None:
            self._items[element_index] = new_item
            self._length += 1
        elif self._items[element_index].key == key:
            self._items[element_index] = new_item

    def __getitem__(self, key: Hashable) -> Any:
        element_index: int = self._find_index(key)
        if self._items[element_index] is None:
            raise KeyError(key)
        return self._items[element_index].value

    def __len__(self) -> int:
        return self._length
