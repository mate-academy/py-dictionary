from __future__ import annotations
from typing import Hashable, Any, Iterator, Iterable

from dataclasses import dataclass


@dataclass
class Pair:
    key: Hashable
    value: Any
    key_hash: int


BucketType = list[Pair]


class Dictionary:

    DEFAULT_CAPACITY: int = 8

    def __init__(
            self,
            capacity: int = DEFAULT_CAPACITY,
            load_factor_limit: float = 0.75
    ) -> None:
        self._buckets: list[BucketType] = [[] for _ in range(capacity)]

        self._load_factor_limit = load_factor_limit

        self._length = 0

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self._load_factor() >= self._load_factor_limit:
            self._resize_and_rehash()

        index = self._index(key)
        bucket = self._buckets[index]
        try:
            index_in_bucket, _ = self._find_pair(bucket, key)
            bucket[index_in_bucket] = Pair(key, value, index)
        except KeyError:
            self._length += 1
            bucket.append(Pair(key, value, index))

    def __getitem__(self, key: Hashable) -> Any:
        bucket = self._buckets[self._index(key)]
        _, pair = self._find_pair(bucket, key)
        return pair.value

    def __delitem__(self, key: Hashable) -> None:
        bucket = self._buckets[self._index(key)]
        index, _ = self._find_pair(bucket, key)
        del bucket[index]
        self._length -= 1

    def __contains__(self, key: Hashable) -> bool:
        try:
            self[key]
        except KeyError:
            return False
        else:
            return True

    def __len__(self) -> int:
        return self._length

    def __iter__(self) -> Iterator:
        yield from self.keys()

    def get(self, key: Hashable, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def items(self) -> list[tuple[Hashable, Any]]:
        return [
            (pair.key, pair.value) for bucket in self._buckets
            for pair in bucket
        ]

    def values(self) -> list[Any]:
        return [pair[1] for pair in self.items()]

    def keys(self) -> list[Hashable]:
        return [pair[0] for pair in self.items()]

    def pop(self, key: Hashable, default: Any = None) -> Any:
        try:
            value = self[key]
            self.__delitem__(key)
            return value
        except KeyError:
            return default

    def update(
            self,
            iterable: Iterable[
                tuple[Hashable, Any]
            ] | Dictionary | dict | None = None,
            **kwargs,
    ) -> None:

        if isinstance(iterable, Dictionary | dict):
            for key, value in iterable.items():
                self[key] = value
        elif isinstance(iterable, Iterable):
            for item in iterable:
                if not isinstance(item, tuple) and len(item) != 2:
                    raise TypeError(
                        f"{type(iterable)} must contain tuples "
                        f"of key-value pairs"
                    )
                self[item[0]] = item[1]
        else:
            raise TypeError(f"{type(iterable)} is not supported")

        for key, value in kwargs.items():
            self[key] = value

    def clear(self) -> None:
        self._buckets = [[] for _ in range(self._capacity())]

    @staticmethod
    def _find_pair(bucket: BucketType, key: Hashable) -> tuple[int, Pair]:
        for index, pair in enumerate(bucket):
            if pair.key == key:
                return index, pair
        raise KeyError(f"{key} not in dict")

    def _capacity(self) -> int:
        return len(self._buckets)

    def _load_factor(self) -> float:
        return len(self) / self._capacity()

    def _index(self, key: Hashable) -> int:
        return hash(key) & (self._capacity() - 1)

    def _resize_and_rehash(self) -> None:
        copy = Dictionary(capacity=self._capacity() * 2)
        for key, value in self.items():
            copy[key] = value
        self._buckets = copy._buckets
