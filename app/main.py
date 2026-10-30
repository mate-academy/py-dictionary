from typing import Any, Iterator


class Node:
    def __init__(self, key: Any, value: Any) -> None:
        self.key = key
        self.hash = hash(key)
        self.value = value


class Dictionary:
    LOAD_FACTOR = 0.75
    INITIAL_CAPACITY = 8

    def __init__(self) -> None:
        self._capacity: int = self.INITIAL_CAPACITY
        self._size: int = 0
        self._buckets: list[list[Node]] = [
            [] for _ in range(self._capacity)
        ]

    def __len__(self) -> int:
        return self._size

    def _get_bucket_index(self, key: Any) -> int:
        return hash(key) % self._capacity

    def _resize(self) -> None:
        old_buckets = self._buckets

        self._capacity *= 2
        self._buckets = [[] for _ in range(self._capacity)]
        self._size = 0

        for bucket in old_buckets:
            for node in bucket:
                self[node.key] = node.value

    def __setitem__(self, key: Any, value: Any) -> None:
        if self._size >= self._capacity * self.LOAD_FACTOR:
            self._resize()

        bucket = self._buckets[self._get_bucket_index(key)]

        for node in bucket:
            if node.key == key:
                node.value = value
                return

        bucket.append(Node(key, value))
        self._size += 1

    def __getitem__(self, key: Any) -> Any:
        bucket = self._buckets[self._get_bucket_index(key)]

        for node in bucket:
            if node.key == key:
                return node.value

        raise KeyError(key)

    def __delitem__(self, key: Any) -> None:
        bucket = self._buckets[self._get_bucket_index(key)]

        for index, node in enumerate(bucket):
            if node.key == key:
                del bucket[index]
                self._size -= 1
                return

        raise KeyError(key)

    def get(self, key: Any, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: Any) -> Any:
        value = self[key]
        del self[key]
        return value

    def clear(self) -> None:
        self._buckets = [[] for _ in range(self._capacity)]
        self._size = 0

    def update(self, other: Iterator[tuple[Any, Any]]) -> None:
        for key, value in other:
            self[key] = value

    def __iter__(self) -> Iterator[Any]:
        for bucket in self._buckets:
            for node in bucket:
                yield node.key

    def items(self) -> Iterator[tuple[Any, Any]]:
        for bucket in self._buckets:
            for node in bucket:
                yield node.key, node.value
