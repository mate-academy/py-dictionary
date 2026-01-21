from typing import Any, Iterator, Optional, List


class _Node:
    __slots__ = ("key", "hash", "value")

    def __init__(self, key: Any, hash_value: int, value: Any) -> None:
        self.key = key
        self.hash = hash_value
        self.value = value


class Dictionary:
    def __init__(self, capacity: int = 8) -> None:
        if capacity <= 0:
            raise ValueError("Capacity must be positive")

        self._capacity: int = capacity
        self._size: int = 0
        self._table: List[List[_Node]] = [[] for _ in range(capacity)]
        self._load_factor: float = 0.75

    def __len__(self) -> int:
        return self._size

    def __setitem__(self, key: Any, value: Any) -> None:
        if self._size / self._capacity >= self._load_factor:
            self._resize()

        hash_value = hash(key)
        index = self._index(hash_value)

        bucket = self._table[index]
        for node in bucket:
            if node.hash == hash_value and node.key == key:
                node.value = value
                return

        bucket.append(_Node(key, hash_value, value))
        self._size += 1

    def __getitem__(self, key: Any) -> Any:
        hash_value = hash(key)
        index = self._index(hash_value)

        bucket = self._table[index]
        for node in bucket:
            if node.hash == hash_value and node.key == key:
                return node.value

        raise KeyError(key)

    def __delitem__(self, key: Any) -> None:
        hash_value = hash(key)
        index = self._index(hash_value)

        bucket = self._table[index]
        for i, node in enumerate(bucket):
            if node.hash == hash_value and node.key == key:
                del bucket[i]
                self._size -= 1
                return

        raise KeyError(key)

    def get(self, key: Any, default: Optional[Any] = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: Any) -> Any:
        value = self[key]
        del self[key]
        return value

    def clear(self) -> None:
        self._table = [[] for _ in range(self._capacity)]
        self._size = 0

    def update(self, other: "Dictionary") -> None:
        for key in other:
            self[key] = other[key]

    def __iter__(self) -> Iterator[Any]:
        for bucket in self._table:
            for node in bucket:
                yield node.key

    def _index(self, hash_value: int) -> int:
        return hash_value % self._capacity

    def _resize(self) -> None:
        old_table = self._table
        self._capacity *= 2
        self._table = [[] for _ in range(self._capacity)]
        self._size = 0

        for bucket in old_table:
            for node in bucket:
                self[node.key] = node.value
