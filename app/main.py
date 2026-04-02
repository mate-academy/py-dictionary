from typing import Any, Iterator
from dataclasses import dataclass


@dataclass
class Node:
    key: Any
    hash_value: int
    value: Any


class Dictionary:
    def __init__(self,
                 initial_capacity: int = 8,
                 load_factor: float = 0.75) -> None:
        self._capacity = initial_capacity
        self._load_factor = load_factor
        self._size = 0
        self._table: list[list[Node]] = [[] for _ in range(self._capacity)]

    def _index(self, key: Any) -> int:
        return hash(key) % self._capacity

    def _find_node(self,
                   key: Any) -> tuple[list[Node], int] | tuple[None, None]:
        index = self._index(key)
        bucket = self._table[index]
        key_hash = hash(key)

        for i, node in enumerate(bucket):
            if node.hash_value == key_hash and node.key == key:
                return bucket, i

        return None, None

    def _resize(self) -> None:
        old_table = self._table
        self._capacity *= 2
        self.clear()

        for bucket in old_table:
            for node in bucket:
                self.__setitem__(node.key, node.value)

    def __setitem__(self, key: Any, value: Any) -> None:
        bucket, index = self._find_node(key)

        if bucket is not None and index is not None:
            bucket[index].value = value
            return

        if (self._size + 1) / self._capacity > self._load_factor:
            self._resize()

        index = self._index(key)
        self._table[index].append(Node(key=key,
                                       hash_value=hash(key),
                                       value=value))
        self._size += 1

    def __getitem__(self, key: Any) -> Any:
        bucket, index = self._find_node(key)

        if bucket is None or index is None:
            raise KeyError(key)

        return bucket[index].value

    def __delitem__(self, key: Any) -> None:
        bucket, index = self._find_node(key)

        if bucket is None or index is None:
            raise KeyError(key)

        del bucket[index]
        self._size -= 1

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[Any]:
        for bucket in self._table:
            for node in bucket:
                yield node.key

    def clear(self) -> None:
        self._table = [[] for _ in range(self._capacity)]
        self._size = 0

    def get(self, key: Any, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: Any, default: Any = None) -> Any:
        try:
            value = self[key]
            del self[key]
            return value
        except KeyError:
            return default

    def update(self, other: Any) -> None:
        if hasattr(other, "items"):
            iterable = other.items()
        else:
            iterable = other

        for key, value in iterable:
            self.__setitem__(key, value)
