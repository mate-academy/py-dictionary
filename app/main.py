from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self._capacity = 8
        self._buckets = [None] * self._capacity
        self._size = 0
        self._load_factor_threshold = 0.75

    def __setitem__(self, key : Any, value: Any) -> None:
        index = hash(key) % self._capacity

        if self._buckets[index] is None:
            self._buckets[index] = [(key, value)]
            self._size += 1
        else:
            for i, (k, v) in enumerate(self._buckets[index]):
                if k == key:
                    self._buckets[index][i] = (key, value)
                    return
            self._buckets[index].append((key, value))
            self._size += 1

        if self._size / self._capacity > self._load_factor_threshold:
            self._resize()

    def _resize(self) -> None:
        old_buckets = self._buckets
        self._capacity *= 2
        self._buckets = [None] * self._capacity
        self._size = 0

        for bucket in old_buckets:
            if bucket:
                for key, value in bucket:
                    self.__setitem__(key, value)

    def __getitem__(self, key: Any) -> bool:
        index = hash(key) % self._capacity
        if self._buckets[index] is None:
            raise KeyError(key)
        else:
            for bucket in self._buckets[index]:
                if bucket[0] == key:
                    return bucket[1]
        raise KeyError(key)

    def __len__(self) -> int:
        return self._size

    def clear(self) -> None:
        self._buckets = [None] * self._capacity
        self._size = 0

    def __delitem__(self, key: Any) -> None:
        index = hash(key) % self._capacity
        bucket = self._buckets[index]
        if self._buckets[index] is None:
            raise KeyError(key)
        else:
            for i, (k, v) in enumerate(bucket):
                if k == key:
                    del bucket[i]
                    self._size -= 1
                    if not bucket:
                        self._buckets[index] = None
                    return
            raise KeyError(key)
