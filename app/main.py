from __future__ import annotations

from dataclasses import dataclass
from typing import Hashable, Any, Union


@dataclass
class Node:
    key: Hashable
    item_hash: int
    value: Any


class Dictionary:
    INITIAL_CAPACITY = 8
    LOAD_FACTOR = 2 / 3

    def __init__(self, buckets: int = INITIAL_CAPACITY) -> None:
        self.__buckets = buckets
        self.__table = [None] * buckets
        self.__size = 0

    def __setitem__(self, key: Hashable, value: Any) -> None:
        existing_bucket = self._find_existing_bucket(key)
        bucket = self._find_empty_bucket(key)
        if existing_bucket is not None:
            self.__table[existing_bucket].value = value
        elif len(self) >= self.__buckets * Dictionary.LOAD_FACTOR:
            self._increase_capacity()
            bucket = self._find_empty_bucket(key)
            self.__table[bucket] = Node(
                key=key,
                item_hash=hash(key),
                value=value
            )
        else:
            self.__table[bucket] = Node(
                key=key,
                item_hash=hash(key),
                value=value
            )
        self.__size += 1

    def __getitem__(self, key: Hashable) -> Any:
        index = self._find_existing_bucket(key=key)
        if index is None:
            raise KeyError(key)
        return self.__table[index].value

    def __len__(self) -> int:
        return sum(1 for item in self.__table if isinstance(item, Node))

    def _find_bucket_index(self, key: Hashable) -> int:
        return hash(key) % len(self.__table)

    def _find_empty_bucket(self, key: Hashable) -> Union[int, None]:
        bucket_index = self._find_bucket_index(key)
        for _ in range(len(self.__table)):
            if self.__table[bucket_index] is None:
                return bucket_index
            bucket_index += 1
            if bucket_index >= len(self.__table):
                bucket_index = 0
        return None

    def _find_existing_bucket(self, key: Hashable) -> Union[int, None]:
        item_hash = hash(key)
        bucket_index = self._find_bucket_index(key)
        while self.__table[bucket_index] is not None:
            if (
                    hash(self.__table[bucket_index].key) == item_hash
                    and self.__table[bucket_index].key == key
            ):
                return bucket_index
            bucket_index += 1
            if bucket_index >= len(self.__table):
                bucket_index = 0
        return None

    def _increase_capacity(self) -> None:
        old_table = self.__table
        self.__buckets *= 2
        self.__table = [None] * self.__buckets
        for bucket in old_table:
            if isinstance(bucket, Node):
                empty_bucket = self._find_empty_bucket(bucket.key)
                self.__table[empty_bucket] = bucket
