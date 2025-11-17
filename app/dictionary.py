from __future__ import annotations
from collections.abc import Hashable, Mapping, Iterator


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

    def _bucket_index(self, key: Hashable) -> int:
        return hash(key) % self.size

    def _resize(self) -> None:
        old_buckets = self.buckets
        self.size *= 2
        self.buckets = [[] for _ in range(self.size)]
        self.count = 0

        for bucket in old_buckets:
            for key, value in bucket:
                self[key] = value

    def __setitem__(self, key: Hashable, value: object) -> None:
        if self.count / self.size > self.load_factor:
            self._resize()

        i = self._bucket_index(key)
        bucket = self.buckets[i]

        for j, (existing_key, _) in enumerate(bucket):
            if key == existing_key:
                bucket[j] = (key, value)
                return

        bucket.append((key, value))
        self.count += 1

    def __getitem__(self, key: Hashable) -> object:
        i = self._bucket_index(key)
        bucket = self.buckets[i]

        for existing_key, value in bucket:
            if key == existing_key:
                return value

        raise KeyError(key)

    def __delitem__(self, key: Hashable) -> None:
        i = self._bucket_index(key)
        bucket = self.buckets[i]

        for j, (existing_key, _) in enumerate(bucket):
            if key == existing_key:
                bucket.pop(j)
                self.count -= 1
                return

        raise KeyError(key)

    def __contains__(self, key: Hashable) -> bool:
        i = self._bucket_index(key)
        bucket = self.buckets[i]

        for existing_key, value in bucket:
            if key == existing_key:
                return True

        return False

    def __iter__(self) -> Iterator[Hashable]:
        for bucket in self.buckets:
            for key, _ in bucket:
                yield key

    def clear(self) -> None:
        self.buckets = [[] for _ in range(self.size)]
        self.count = 0

    def update(self, other: Mapping) -> None:
        for key, value in other.items():
            self[key] = value

    def pop(self, key: Hashable, default: object = None) -> object:
        i = self._bucket_index(key)
        bucket = self.buckets[i]

        for j, (existing_key, value) in enumerate(bucket):
            if key == existing_key:
                bucket.pop(j)
                self.count -= 1
                return value

        if default is not None:
            return default

        raise KeyError(key)

    def keys(self) -> Iterator:
        for key in self:
            yield key

    def values(self) -> Iterator:
        for bucket in self.buckets:
            for _, value in bucket:
                yield value

    def items(self) -> Iterator:
        for bucket in self.buckets:
            for key, value in bucket:
                yield key, value
