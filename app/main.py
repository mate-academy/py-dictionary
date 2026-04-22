from typing import Any
from dataclasses import dataclass


@dataclass
class DictItem:
    item_key: Any
    item_hash: int
    item_value: Any


_unique = object()


class Dictionary:
    def __init__(self) -> None:
        self._capacity: int = 8
        self._length: int = 0

        self._table: list[DictItem | None] = [None] * self._capacity

        self._load_factor: float = 2 / 3
        self._DUMMY = DictItem(None, -1, None)

    def get(self, key: Any, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: Any, default: Any = _unique) -> Any:
        try:
            value = self[key]
            del self[key]
            return value
        except KeyError:
            if default is not _unique:
                return default
            raise KeyError(f"Key not found: {key}")

    def update(self, other: DictItem) -> None:
        for item in other:
            if item is not self._DUMMY:
                self[item.item_key] = item.item_value

    def clear(self) -> None:
        self._capacity = 8
        self._length = 0
        self._table = [None for _ in range(self._capacity)]

    def _get_hash_and_index(self, key: Any) -> int:
        key_hash = hash(key)
        return key_hash, key_hash % self._capacity

    def _resize_table(self) -> None:
        old_table = self._table
        self._capacity *= 2
        self._table = [None for _ in range(self._capacity)]
        self._length = 0

        for item in old_table:
            if item is not None and item is not self._DUMMY:
                index = item.item_hash % self._capacity
                while self._table[index] is not None:
                    index = (index + 1) % self._capacity
                self._table[index] = item
                self._length += 1

    def __setitem__(self, key: Any, value: Any) -> None:
        if (len(self) + 1) / self._capacity >= self._load_factor:
            self._resize_table()
        key_hash, key_index = self._get_hash_and_index(key)

        dummy_index = None
        while self._table[key_index] is not None:
            item = self._table[key_index]
            if item is self._DUMMY and dummy_index is None:
                dummy_index = key_index
            if item.item_hash == key_hash and item.item_key == key:
                item.item_value = value
                return
            key_index = (key_index + 1) % self._capacity

        if dummy_index is not None:
            key_index = dummy_index

        self._table[key_index] = DictItem(key, key_hash, value)
        self._length += 1

    def __getitem__(self, key: Any) -> Any:
        key_hash, key_index = self._get_hash_and_index(key)

        while self._table[key_index] is not None:
            item = self._table[key_index]
            if (item is not self._DUMMY and item.item_hash == key_hash
                    and item.item_key == key):
                return item.item_value
            key_index = (key_index + 1) % self._capacity

        raise KeyError(f"Key not found: {key}")

    def __delitem__(self, key: Any) -> Any:
        key_hash, key_index = self._get_hash_and_index(key)

        while self._table[key_index] is not None:
            item = self._table[key_index]
            if (item is not self._DUMMY and item.item_hash == key_hash
                    and item.item_key == key):
                self._table[key_index] = self._DUMMY
                self._length -= 1
                return
            key_index = (key_index + 1) % self._capacity

        raise KeyError(f"Key not found: {key}")

    def __iter__(self) -> Any:
        for item in self._table:
            if item is not None and item is not self._DUMMY:
                yield item.item_key

    def __len__(self) -> int:
        return self._length

    def __str__(self) -> str:
        items = [
            f"{item.item_key}: {item.item_value}"
            for item in self._table
            if item is not None and item is not self._DUMMY
        ]
        dict_str = "{" + ", ".join(items) + "}"
        return f"{self.__class__.__name__} {dict_str}"

    def __repr__(self) -> str:
        return (f"{self.__str__()}, len={self._length}, "
                f"capacity={self._capacity}")
