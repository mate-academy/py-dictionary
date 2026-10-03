from typing import Any, Optional


class Point:
    def __init__(self, x: float, y: float) -> None:
        self._x = x
        self._y = y

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y


class Node:
    def __init__(self, key: Any, value: Any, key_hash: int) -> None:
        self.key = key
        self.value = value
        self.hash = key_hash


class Dictionary:
    def __init__(self, capacity: int = 8, load_factor: float = 0.75) -> None:
        self._capacity = capacity
        self._load_factor = load_factor
        self._size = 0
        self._buckets: list[Optional[list[Node]]] = [None] * self._capacity

    def __len__(self) -> int:
        return self._size

    def _get_bucket_index(self, key_hash: int, capacity: int) -> int:
        return key_hash % capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        if self._size / self._capacity >= self._load_factor:
            self._resize()

        key_hash = hash(key)
        index = self._get_bucket_index(key_hash, self._capacity)

        if self._buckets[index] is None:
            self._buckets[index] = []

        bucket = self._buckets[index]
        for node in bucket:
            if node.hash == key_hash and node.key == key:
                node.value = value
                return

        bucket.append(Node(key, value, key_hash))
        self._size += 1

    def __getitem__(self, key: Any) -> Any:
        key_hash = hash(key)
        index = self._get_bucket_index(key_hash, self._capacity)

        bucket = self._buckets[index]
        if bucket is not None:
            for node in bucket:
                if node.hash == key_hash and node.key == key:
                    return node.value

        raise KeyError(f"Key not found: {key}")

    def _resize(self) -> None:
        old_buckets = self._buckets
        self._capacity *= 2
        self._size = 0
        self._buckets = [None] * self._capacity

        for bucket in old_buckets:
            if bucket is not None:
                for node in bucket:
                    self.__setitem__(node.key, node.value)
