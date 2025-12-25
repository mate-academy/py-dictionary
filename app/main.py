from enum import Enum
from typing import Any, Iterator, Hashable


class Bucket(Enum):
    DELETED = object()
    HASH = 0
    KEY = 1
    VALUE = 2


class Dictionary:
    """
    Custom hash map implementation with open addressing.
    Uses linear probing to resolve hash collisions.
    Each bucket structured as [HASH, KEY, VALUE] using the Bucket enum.
    """
    def __init__(self, **kwargs) -> None:
        self._size: int = 0
        self._capacity: int = 8
        self._threshold: int = 5
        self._hash_map: list[list | None] = [None] * self._capacity

        for key, value in kwargs.items():
            self[key] = value

    def get(self, key: Hashable, default: Any = None) -> Any:
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def pop(self, key: Hashable, default: Any = None) -> Any:
        try:
            value = self.__getitem__(key)
        except KeyError:
            if default is not None:
                return default
            raise

        self.__delitem__(key)
        return value

    def update(self, other: dict | tuple = None, **kwargs) -> None:
        if other is not None:
            if hasattr(other, "keys"):
                for key in other:
                    self.__setitem__(key, other.get(key))
            else:
                for key, value in other:
                    self.__setitem__(key, value)

        for key, value in kwargs.items():
            self.__setitem__(key, value)

    def clear(self) -> None:
        self._size = 0
        self._capacity = 8
        self._threshold = 5
        self._hash_map = [None] * 8

    def _insert_item(self, key: Hashable, value: Any) -> None:
        key_hash = hash(key)
        index = key_hash % self._capacity

        for i in range(self._capacity):
            probe_index = (index + i) % self._capacity
            bucket = self._hash_map[probe_index]

            if bucket is None or bucket is Bucket.DELETED.value:
                self._hash_map[probe_index] = [key_hash, key, value]
                self._size += 1
                break
            elif key == bucket[Bucket.KEY.value]:
                self._hash_map[probe_index] = [key_hash, key, value]
                break

    def _resize(self, new_capacity: int) -> None:
        self._size = 0
        self._capacity = new_capacity
        self._threshold = int(self._capacity * 2 / 3)

        old_hash_map = self._hash_map
        self._hash_map = [None] * self._capacity

        for bucket in old_hash_map:
            if bucket is not None and bucket is not Bucket.DELETED.value:
                self._insert_item(
                    bucket[Bucket.KEY.value],
                    bucket[Bucket.VALUE.value]
                )

    def _resize_up(self) -> None:
        self._resize(self._capacity * 2)

    def _resize_down(self) -> None:
        self._resize(self._capacity // 2)

    def __setitem__(self, key: Hashable, value: Any) -> None:
        self._insert_item(key, value)

        if self._size >= self._threshold:
            self._resize_up()

    def __getitem__(self, key: Hashable) -> Any:
        index = hash(key) % self._capacity

        for i in range(self._capacity):
            probe_index = (index + i) % self._capacity
            bucket = self._hash_map[probe_index]

            if bucket is None:
                raise KeyError(key)
            elif bucket is Bucket.DELETED.value:
                continue
            elif bucket[Bucket.KEY.value] == key:
                return bucket[Bucket.VALUE.value]

        raise KeyError(key)

    def __delitem__(self, key: Hashable) -> None:
        index = hash(key) % self._capacity

        for i in range(self._capacity):
            probe_index = (index + i) % self._capacity
            bucket = self._hash_map[probe_index]

            if bucket is None:
                break
            if bucket[Bucket.KEY.value] == key:
                self._hash_map[probe_index] = Bucket.DELETED.value
                self._size -= 1

                if self._size <= self._capacity // 4 and self._capacity > 8:
                    self._resize_down()

                return

        raise KeyError(key)

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator:
        return (
            bucket[Bucket.KEY.value] for bucket in self._hash_map if
            bucket is not None and bucket is not Bucket.DELETED.value
        )

    def __repr__(self) -> str:
        items = []
        for bucket in self._hash_map:
            if bucket is not None and bucket is not Bucket.DELETED.value:
                items.append(
                    f"{bucket[Bucket.KEY.value]}: {bucket[Bucket.VALUE.value]}"
                )
        return "{" + ", ".join(items) + "}"
