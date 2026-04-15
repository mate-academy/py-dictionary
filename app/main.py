from typing import Any, List


class Node:
    def __init__(self, key: Any, value: Any, hash_value: int) -> None:
        self.key = key
        self.value = value
        self.hash_value = hash_value


class Dictionary:
    def __init__(self, capacity: int = 8) -> None:
        if capacity <= 0:
            capacity = 8

        self.capacity: int = capacity
        self.size: int = 0
        self.load_factor: float = 0.75
        self.buckets: List[List[Node]] = [[] for _ in range(self.capacity)]

    def _get_bucket_index(self, key_hash: int) -> int:
        return key_hash % self.capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        try:
            key_hash = hash(key)
        except TypeError:
            raise TypeError(
                f"unhashable type: '{type(key).__name__}'"
            )

        index = self._get_bucket_index(key_hash)
        bucket = self.buckets[index]

        for node in bucket:
            if node.key == key:
                node.value = value
                return

        bucket.append(Node(key, value, key_hash))
        self.size += 1

        if self.size / self.capacity > self.load_factor:
            self._resize()

    def __getitem__(self, key: Any) -> Any:
        try:
            key_hash = hash(key)
        except TypeError:
            raise TypeError(
                f"unhashable type: '{type(key).__name__}'"
            )

        index = self._get_bucket_index(key_hash)
        bucket = self.buckets[index]

        for node in bucket:
            if node.key == key:
                return node.value

        raise KeyError(key)

    def __len__(self) -> int:
        return self.size

    def _resize(self) -> None:
        old_buckets = self.buckets

        self.capacity *= 2
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0

        for bucket in old_buckets:
            for node in bucket:
                index = self._get_bucket_index(node.hash_value)
                self.buckets[index].append(node)
                self.size += 1
