from typing import Any, Optional, List


class _Node:
    def __init__(self, key: Any, value: Any) -> None:
        self.key = key
        self.hash = hash(key)
        self.value = value


class Dictionary:
    def __init__(
            self,
            initial_capacity: int = 8,
            load_factor: float = 0.75
    ) -> None:
        if initial_capacity <= 0:
            raise ValueError("initial_capacity must be positive")

        self._capacity: int = initial_capacity
        self._buckets: List[Optional[list[_Node]]] = [None] * self._capacity
        self._size: int = 0
        self._load_factor: float = load_factor

    def __len__(self) -> int:
        return self._size

    def _bucket_index(self, key_hash: int) -> int:
        return key_hash % self._capacity

    def _resize_if_needed(self) -> None:
        if self._size / self._capacity <= self._load_factor:
            return

        old_buckets = self._buckets
        self._capacity *= 2
        self._buckets = [None] * self._capacity
        self._size = 0

        for bucket in old_buckets:
            if bucket is None:
                continue
            for node in bucket:
                self[node.key] = node.value

    def __setitem__(self, key: Any, value: Any) -> None:
        key_hash = hash(key)
        index = self._bucket_index(key_hash)

        bucket = self._buckets[index]
        if bucket is None:
            bucket = []
            self._buckets[index] = bucket

        for node in bucket:
            if node.hash == key_hash and node.key == key:
                node.value = value
                return

        bucket.append(_Node(key, value))
        self._size += 1
        self._resize_if_needed()

    def __getitem__(self, key: Any) -> Any:
        key_hash = hash(key)
        index = self._bucket_index(key_hash)
        bucket = self._buckets[index]

        if bucket is None:
            raise KeyError(key)

        for node in bucket:
            if node.hash == key_hash and node.key == key:
                return node.value

        raise KeyError(key)
