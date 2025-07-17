from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Iterable, Generator


class DictionaryIterator:
    def __init__(self, dictionary: Dictionary) -> None:
        self._dict = dictionary
        self._idx = 0

    def __iter__(self) -> DictionaryIterator:
        self._idx = 0
        return self

    def __next__(self) -> Any:
        while (
            self._idx < len(self._dict._order)
            and self._dict._order[self._idx] is None
        ):
            self._idx += 1

        if self._idx >= len(self._dict._order):
            raise StopIteration

        element = self._dict._items[self._dict._order[self._idx]].key
        self._idx += 1
        return element


class DictionaryKeys:
    def __init__(self, dictionary: Dictionary) -> None:
        self._dict = dictionary

    def __iter__(self) -> Generator:
        for index in self._dict._order:
            if index is not None:
                yield self._dict._items[index].key


class DictionaryValues:
    def __init__(self, dictionary: Dictionary) -> None:
        self._dict = dictionary

    def __iter__(self) -> Generator:
        for index in self._dict._order:
            if index is not None:
                yield self._dict._items[index].value


class DictionaryItems:
    def __init__(self, dictionary: Dictionary) -> None:
        self._dict = dictionary

    def __iter__(self) -> Generator:
        for index in self._dict._order:
            if index is not None:
                item = self._dict._items[index]
                yield (item.key, item.value)


class NoneItem:
    _instance = None

    def __new__(cls, *args, **kwargs) -> NoneItem:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


NONE = NoneItem()


@dataclass
class Item:
    key: Any
    hash_key: int
    value: Any
    order_idx: int

    def __repr__(self) -> str:
        return f"{self.key.__repr__()}: {self.value.__repr__()}"


class Dictionary:
    DEFAULT_CAPACITY: int = 8
    DEFAULT_LOAD_FACTOR: float = 2 / 3

    def __init__(self) -> None:
        self._capacity: int = Dictionary.DEFAULT_CAPACITY
        self._load_factor: float = Dictionary.DEFAULT_LOAD_FACTOR
        self._threshold: int = int(self._capacity * self._load_factor)
        self._length: int = 0
        self._items: list[Item | None] = [None] * self._capacity
        self._order: list = []

    def _resize(self) -> None:
        self._capacity *= 2
        self._threshold = int(self._capacity * self._load_factor)
        self._length = 0

        temp_items = self._items
        temp_order = self._order.copy()
        self._order.clear()
        self._items = [None] * self._capacity

        for idx in temp_order:
            if idx is not None:
                self[temp_items[idx].key] = temp_items[idx].value

    def _find_free_index(self, key: Any, hash_key: int) -> int:
        idx: int = hash_key % self._capacity

        while self._items[idx]:
            if (
                self._items[idx] is not NONE
                and key == self._items[idx].key
            ):
                break
            idx = (idx + 1) % self._capacity

        return idx

    def _find_index(self, key: Any) -> int:
        hash_key = hash(key)
        idx: int = hash_key % self._capacity

        while (
            self._items[idx] is NONE
            or (self._items[idx] and key != self._items[idx].key)
        ):
            idx = (idx + 1) % self._capacity

        if not self._items[idx]:
            raise KeyError
        return idx

    def __setitem__(self, key: Any, value: Any) -> None:
        if self._length >= self._threshold:
            self._resize()

        hash_key = hash(key)
        idx: int = self._find_free_index(key, hash_key)

        if self._items[idx]:
            self._items[idx].value = value
            return

        self._length += 1
        self._items[idx] = Item(
            key=key,
            hash_key=hash_key,
            value=value,
            order_idx=len(self._order)
        )
        self._order.append(idx)

    def __getitem__(self, key: Any) -> Any:
        idx: int = self._find_index(key)
        return self._items[idx].value

    def clear(self) -> None:
        self._capacity: int = Dictionary.DEFAULT_CAPACITY
        self._threshold: int = int(self._capacity * self._load_factor)
        self._length = 0
        self._items: list[Item | None] = [None] * self._capacity
        self._order.clear()

    def __delitem__(self, key: Any) -> None:
        idx: int = self._find_index(key)
        self._length -= 1
        item = self._items[idx]
        self._order[item.order_idx] = None
        self._items[idx] = NONE

    def __contains__(self, key: Any) -> bool:
        try:
            self._find_index(key)
            return True
        except KeyError:
            return False

    def get(self, key: Any, default_value: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default_value

    def pop(self, key: Any, default: NoneItem | Any = NONE) -> Any:
        try:
            item = self[key]
            del self[key]
            return item
        except KeyError:
            if default is NONE:
                raise
            return default

    def update(self, iterable: Iterable) -> None:
        if isinstance(iterable, (Dictionary, dict)):
            for key, value in iterable.items():
                self[key] = value
        else:
            for key, value in iterable:
                self[key] = value

    def __iter__(self) -> DictionaryIterator:
        return DictionaryIterator(self)

    def __len__(self) -> int:
        return self._length

    def keys(self) -> DictionaryKeys:
        return DictionaryKeys(self)

    def values(self) -> DictionaryValues:
        return DictionaryValues(self)

    def items(self) -> DictionaryItems:
        return DictionaryItems(self)

    def __repr__(self) -> str:
        items_repr = str([
            self._items[key]
            for key in self._order if key is not None
        ])[1:-1]
        return f"{{{items_repr}}}"

    def __str__(self) -> str:
        return self.__repr__()
