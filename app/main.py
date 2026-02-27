from typing import Any


class Node:
    def __init__(self, key: object, hash_value: int, value: object) -> None:
        self.key = key
        self.hash = hash_value
        self.value = value


class Dictionary:
    def __init__(self, capacity: int = 8) -> None:
        self._capacity = capacity
        self._size = 0
        self._buckets = [[] for _ in range(self._capacity)]
        self._load_factor = 0.75

    def __len__(self) -> int:
        return self._size

    def __setitem__(self, key: Any, value: Any) -> None:
        node_hash = hash(key)
        index = node_hash % self._capacity
        bucket = self._buckets[index]

        for node in bucket:
            if node.key == key:
                node.value = value
                return

        bucket.append(Node(key, hash(key), value))
        self._size += 1

        if self._size / self._capacity > self._load_factor:
            self.resize()

    def __getitem__(self, key: Any) -> Any:
        node_hash = hash(key)
        index = node_hash % self._capacity
        bucket = self._buckets[index]

        for node in bucket:
            if node.key == key:
                return node.value

        raise KeyError(key)

    def resize(self) -> None:
        old_buckets = self._buckets
        self._capacity *= 2
        self._buckets = [[] for _ in range(self._capacity)]
        self._size = 0

        for bucket in old_buckets:
            for node in bucket:
                index = node.hash % self._capacity
                self._buckets[index].append(node)
                self._size += 1

    def clear(self) -> None:
        self._buckets = [[] for _ in range(self._capacity)]
        self._size = 0

    def __delitem__(self, key: Any) -> None:
        index = hash(key) % self._capacity
        bucket = self._buckets[index]

        for i, node in enumerate(bucket):
            if node.key == key:
                del bucket[i]
                self._size -= 1
                return

        raise KeyError(key)

    def get(self, key: Any, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: Any, default: Any = None) -> Any:
        index = hash(key) % self._capacity
        bucket = self._buckets[index]

        for i, node in enumerate(bucket):
            if node.key == key:
                value = node.value
                del bucket[i]
                self._size -= 1
                return value

        if default is not None:
            return default

        raise KeyError(key)
