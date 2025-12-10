from __future__ import annotations
from collections.abc import Hashable, Mapping, Iterator


class Node:
    __slots__ = ("key", "hash", "value")

    def __init__(self, key: Hashable, hash_value: int, value: object) -> None:
        self.key = key
        self.hash = hash_value
        self.value = value


class Dictionary:
    def __init__(self, size: int = 8) -> None:
        if size < 0:
            raise ValueError("size must be non-negative")

        self.size = size
        self.buckets = [[] for _ in range(size)]
        self.count = 0
        self.load_factor = 3 / 4

    def __len__(self) -> int:
        return self.count

    def _bucket_index(self, key_hash: int) -> int:
        return key_hash % self.size

    def _resize(self) -> None:
        old_buckets = self.buckets

        self.size *= 2
        self.buckets = [[] for _ in range(self.size)]
        self.count = 0

        for bucket in old_buckets:
            for node in bucket:
                self[node.key] = node.value

    def __setitem__(self, key: Hashable, value: object) -> None:
        if self.count / self.size > self.load_factor:
            self._resize()

        key_hash = hash(key)
        i = self._bucket_index(key_hash)
        bucket = self.buckets[i]
        for node in bucket:
            if node.key == key:
                node.value = value
                return

        bucket.append(Node(key, key_hash, value))
        self.count += 1

    def __getitem__(self, key: Hashable) -> object:
        key_hash = hash(key)
        i = self._bucket_index(key_hash)
        bucket = self.buckets[i]
        for node in bucket:
            if node.key == key:
                return node.value

        raise KeyError(key)

    def __delitem__(self, key: Hashable) -> None:
        key_hash = hash(key)
        i = self._bucket_index(key_hash)
        bucket = self.buckets[i]
        for index, node in enumerate(bucket):
            if node.key == key:
                bucket.pop(index)
                self.count -= 1
                return

        raise KeyError(key)

    def __contains__(self, key: Hashable) -> bool:
        key_hash = hash(key)
        i = self._bucket_index(key_hash)
        bucket = self.buckets[i]
        for node in bucket:
            if node.key == key:
                return True

        return False

    def __iter__(self) -> Iterator[Hashable]:
        for bucket in self.buckets:
            for node in bucket:
                yield node.key

    def clear(self) -> None:
        self.buckets = [[] for _ in range(self.size)]
        self.count = 0

    def update(self, other: Mapping) -> None:
        for key, value in other.items():
            self[key] = value

    def pop(self, key: Hashable, default: object = None) -> object:
        key_hash = hash(key)
        i = self._bucket_index(key_hash)
        bucket = self.buckets[i]
        for index, node in enumerate(bucket):
            if node.key == key:
                bucket.pop(index)
                self.count -= 1
                return node.value

        if default is not None:
            return default

        raise KeyError(key)

    def keys(self) -> Iterator:
        for key in self:
            yield key

    def values(self) -> Iterator:
        for bucket in self.buckets:
            for node in bucket:
                yield node.value

    def items(self) -> Iterator:
        for bucket in self.buckets:
            for node in bucket:
                yield node.key, node.value
