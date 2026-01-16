from typing import Any, Iterator, Hashable


class Node:
    def __init__(self, key: Hashable, value: Any) -> None:
        self.key = key
        self.hash = hash(key)
        self.value = value

    def __eq__(self, other: Any) -> bool:
        return self.hash == other.hash and self.key == other.key


class Dictionary:
    def __init__(
            self,
            initial_capacity: int | float = 8,
            load_factor: int | float = (2 / 3)
    ) -> None:
        self.capacity = initial_capacity
        self.size = 0
        self.load_factor = load_factor
        self.buckets = [[] for _ in range(self.capacity)]

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.size / self.capacity > self.load_factor:
            self._resize()

        index = hash(key) % self.capacity
        bucket = self.buckets[index]

        for node in bucket:
            if node.key == key:
                node.value = value
                return

        bucket.append(Node(key, value))
        self.size += 1

    def __getitem__(self, key: Hashable) -> Any:
        index = hash(key) % self.capacity
        bucket = self.buckets[index]

        for node in bucket:
            if node.key == key:
                return node.value

        raise KeyError(f"Key '{key}' not found.")

    def __len__(self) -> int:
        return self.size

    def __delitem__(self, key: Hashable) -> None:
        index = hash(key) % self.capacity
        bucket = self.buckets[index]

        for i, node in enumerate(bucket):
            if node.key == key:
                del bucket[i]
                self.size -= 1
                return

        raise KeyError(f"Key '{key}' not found.")

    def get(self, key: Hashable, default: Hashable = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: Hashable, default: Hashable = None) -> Any:
        index = hash(key) % self.capacity
        bucket = self.buckets[index]

        for i, node in enumerate(bucket):
            if node.key == key:
                value = node.value
                del bucket[i]
                self.size -= 1
                return value

        if default is not None:
            return default
        raise KeyError(f"Key '{key}' not found.")

    def clear(self) -> None:
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0

    def update(self, other: Any) -> None:
        for key in other:
            self[key] = other[key]

    def __iter__(self) -> Iterator[Any]:
        for bucket in self.buckets:
            for node in bucket:
                yield node.key

    def _resize(self) -> None:
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0

        for bucket in old_buckets:
            for node in bucket:
                self[node.key] = node.value
