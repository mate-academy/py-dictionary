from typing import Any, Iterator, Optional


class Dictionary:
    INITIAL_CAPACITY = 8
    LOAD_FACTOR_THRESHOLD = 2 / 3

    def __init__(self, data: Any = None) -> None:
        self._capacity = self.INITIAL_CAPACITY
        self._table: list[Optional[list[tuple[Any, Any]]]] = [
            None for _ in range(self._capacity)
        ]
        self._length = 0

        if data is not None:
            self.update(data)

    def _get_bucket_index(self, key: Any) -> int:
        return hash(key) % self._capacity

    def _resize(self) -> None:
        old_table = self._table
        self._capacity *= 2
        self._table = [None for _ in range(self._capacity)]
        self._length = 0

        for bucket in old_table:
            if bucket is not None:
                for key, value in bucket:
                    self[key] = value

    def __getitem__(self, key: Any) -> Any:
        index = self._get_bucket_index(key)
        bucket = self._table[index]

        if bucket is not None:
            for k, v in bucket:
                if k == key:
                    return v

        raise KeyError(f"Key '{key}' not found in Dictionary.")

    def __setitem__(self, key: Any, value: Any) -> None:
        if (self._length + 1) / self._capacity > self.LOAD_FACTOR_THRESHOLD:
            self._resize()

        index = self._get_bucket_index(key)
        bucket = self._table[index]

        if bucket is None:
            self._table[index] = [(key, value)]
            self._length += 1
        else:
            for idx, (k, _) in enumerate(bucket):
                if k == key:
                    bucket[idx] = (key, value)
                    return
            bucket.append((key, value))
            self._length += 1

    def __delitem__(self, key: Any) -> None:
        index = self._get_bucket_index(key)
        bucket = self._table[index]

        if bucket is not None:
            for idx, (k, _) in enumerate(bucket):
                if k == key:
                    bucket.pop(idx)
                    self._length -= 1
                    return

        raise KeyError(f"Key '{key}' not found in Dictionary.")

    def __len__(self) -> int:
        return self._length

    def __iter__(self) -> Iterator[Any]:
        for bucket in self._table:
            if bucket is not None:
                for key, _ in bucket:
                    yield key

    def items(self) -> Iterator[tuple[Any, Any]]:
        for bucket in self._table:
            if bucket is not None:
                for item in bucket:
                    yield item

    def update(self, other: Any = None, **kwargs: Any) -> None:
        if other is not None:
            if hasattr(other, "items"):
                for key, value in other.items():
                    self[key] = value
            else:
                for key in other:
                    self[key] = other[key]

        for key, value in kwargs.items():
            self[key] = value

    def clear(self) -> None:
        self._capacity = self.INITIAL_CAPACITY
        self._table = [None for _ in range(self._capacity)]
        self._length = 0

    def get(self, key: Any, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default
