from typing import Hashable, Any
from collections import namedtuple

Bucket = namedtuple(
    "Bucket", ["key", "hashed_key", "value", "is_deleted"]
)


class Dictionary:
    def __init__(self) -> None:
        self._length = 0
        self._capacity = 8
        self._table: list[None | Bucket] = [None] * self._capacity
        self._threshold = int(self._capacity * (2 / 3))

    def __repr__(self) -> str:
        items = [
            f"{item.key}: {item.value}"
            for item in self._table
            if item is not None
        ]
        return "{" + ", ".join(items) + "}"

    def __getitem__(self, key: Hashable) -> Any:
        index = self._get_hash_index(key)

        while True:
            if self._table[index] is None:
                raise KeyError(f"Key `{key}` is not found!")
            if (
                    self._table[index] is not None
                    and self._table[index].key == key
            ):
                return self._table[index].value

            index = self._increment_index(index)

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self._get_hash_index(key)

        while True:
            if self._table[index] is None or self._table[index].is_deleted:
                self._length += 1

                if self._length >= self._threshold:
                    self.__resize()
                    self[key] = value

                self._table[index] = Bucket(
                    key, hash(key), value, is_deleted=False
                )
                break

            if self._table[index].key == key:
                self._table[index] = Bucket(
                    key, hash(key), value, is_deleted=False
                )
                break

            index = self._increment_index(index)

    def __delitem__(self, key: Hashable) -> None:
        index = self._get_hash_index(key)

        while True:
            if (
                    self._table[index] is not None
                    and self._table[index].key == key
            ):
                self._table[index] = Bucket(
                    None, None, None, is_deleted=True
                )
                self._length -= 1
                break

            if self._table[index] is None:
                raise KeyError(f"Key `{key}` is not found!")

            index = self._increment_index(index)

    def __len__(self) -> int:
        return self._length

    def _get_hash_index(self, key: Hashable) -> int:
        return hash(key) % self._capacity

    def _increment_index(self, index: int) -> int:
        return (index + 1) % self._capacity

    def __resize(self) -> None:
        self._capacity *= 2
        self._threshold = int(self._capacity * (2 / 3))
        self._length = 0

        old_table = self._table
        self._table = [None] * self._capacity

        for item in old_table:
            if item is not None:
                self[item.key] = item.value

    def get(self, key: Hashable, value: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return value

    def clear(self) -> None:
        self._capacity = 8
        self._table = [None] * self._capacity
        self._length = 0
        self._threshold = int(self._capacity * (2 / 3))
