from typing import Any


class Node:
    def __init__(self, key: int, hash_: int, value: Any) -> None:
        self.key = key
        self.hash = hash_
        self.value = value


class Dictionary:
    def __init__(self, capacity: int = 8) -> None:
        self.capacity = capacity
        self.length = 0
        self.load_factor = 0.75
        self.buckets = [[] for _ in range(self.capacity)]

    def _hash(self, key: int) -> int:
        return hash(key)

    def _get_index(self, hash_: int) -> int:
        return hash_ % self.capacity

    def _resize(self) -> None:
        old_buckets = self.buckets

        self.capacity *= 2
        self.buckets = [[] for _ in range(self.capacity)]

        for bucket in old_buckets:
            for node in bucket:
                index = self._get_index(node.hash)
                self.buckets[index].append(node)

    def __setitem__(self, key: int, value: Any) -> None:
        hash_ = self._hash(key)
        index = self._get_index(hash_)
        bucket = self.buckets[index]

        for node in bucket:
            if node.key == key:
                node.value = value
                return

        bucket.append(Node(key, hash_, value))
        self.length += 1

        if self.length / self.capacity > self.load_factor:
            self._resize()

    def __getitem__(self, key: int) -> Any:
        hash_ = self._hash(key)
        index = self._get_index(hash_)
        bucket = self.buckets[index]

        for node in bucket:
            if node.key == key:
                return node.value

        raise KeyError(f"Key '{key}' not found")

    def __delitem__(self, key: int) -> None:
        hash_ = self._hash(key)
        index = self._get_index(hash_)
        bucket = self.buckets[index]

        for i, node in enumerate(bucket):
            if node.key == key:
                bucket.pop(i)
                self.length -= 1
                return

        raise KeyError(f"Key '{key}' not found")

    def __len__(self) -> int:
        return self.length
