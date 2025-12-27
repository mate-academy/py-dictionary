from dataclasses import dataclass
from typing import Hashable, Any, Iterator, Iterable


class Dictionary:

    INITIAL_CAPACITY = 8
    RESIZE_THRESHOLD = 2 / 3

    @dataclass
    class Bucket:
        key: Hashable
        value: Any

        def __str__(self) -> str:
            return f"{self.key}: {self.value}"

    def __init__(self, capacity: int = INITIAL_CAPACITY) -> None:
        self._capacity = capacity
        self._size = 0
        self._table: list[Dictionary.Bucket | None] = [None] * self._capacity

    def _calculate_index(self, key: Hashable) -> int:
        index = hash(key) % self._capacity

        while (self._table[index] is not None
               and self._table[index].key != key):
            index = (index + 1) % self._capacity

        return index

    @property
    def current_max_size(self) -> float | int:
        return self._capacity * Dictionary.RESIZE_THRESHOLD

    def resize(self) -> None:
        old_hash_table = self._table
        new_size = self._capacity * 2

        self.__init__(new_size)

        for node in old_hash_table:
            if node is not None:
                self.__setitem__(node.key, node.value)

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self._calculate_index(key)

        if self._table[index] is None:
            if self._size + 1 >= self.current_max_size:
                self.resize()
                return self.__setitem__(key, value)

            self._size += 1

        self._table[index] = Dictionary.Bucket(key, value)

    def __getitem__(self, key: Hashable) -> Any:
        index = self._calculate_index(key)

        if self._table[index] is None:
            raise KeyError(f"Cannot find value for key: {key}")

        return self._table[index].value

    def __len__(self) -> int:
        return self._size

    def _rehash_all(self) -> None:
        existing_buckets = [
            bucket for bucket
            in self._table
            if bucket is not None
        ]

        self.__init__(self._capacity)

        for bucket in existing_buckets:
            self.__setitem__(bucket.key, bucket.value)

    def __delitem__(self, key: Hashable) -> None:
        index = self._calculate_index(key)

        if self._table[index] is None:
            raise KeyError(f"Cannot find value for key: {key}")

        self._table[index] = None
        self._size -= 1
        self._rehash_all()

    def get(self, key: Hashable, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: Hashable, default: Any = None) -> Any:
        try:
            value = self[key]
        except KeyError:
            if default is not None:
                return default
            raise

        self.__delitem__(key)
        return value

    def clear(self) -> None:
        self.__init__()

    def update(self, other: Iterable[Any] = None, **kwargs) -> None:
        if other:
            if hasattr(other, "items"):
                for key, value in other.items():
                    self[key] = value
            elif hasattr(other, "__iter__"):
                for item in other:
                    if isinstance(item, (list, tuple)) and len(item) == 2:
                        key, value = item
                        self[key] = value
                    else:
                        raise ValueError
            else:
                raise ValueError

        for key, value in kwargs.items():
            self[key] = value

    def keys(self) -> Iterator[Hashable]:
        for bucket in self._table:
            if bucket is not None:
                yield bucket.key

    def values(self) -> Iterator[Any]:
        for bucket in self._table:
            if bucket is not None:
                yield bucket.value

    def items(self) -> Iterator[tuple[Hashable, Any]]:
        for bucket in self._table:
            if bucket is not None:
                yield bucket.key, bucket.value

    def __iter__(self) -> Iterator[Hashable]:
        return self.keys()

    def __str__(self) -> str:
        items = {
            bucket.key: bucket.value
            for bucket in self._table
            if bucket is not None
        }
        return str(items)
