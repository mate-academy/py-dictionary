from typing import Any, Optional, Iterator


class Dictionary:
    def __init__(
            self,
            initial_capacity: int = 8,
            load_factor: float = 0.75
    ) -> None:
        self.load_factor = load_factor
        self.capacity = initial_capacity
        self.size = 0
        self.buckets: list[Optional[list[Any]]] = [None] * initial_capacity

    class Node:
        def __init__(self, key: Any, value: Any) -> None:
            self.key = key
            self.value = value
            self.hash = hash(key)

    def _resize(self) -> None:
        new_capacity = self.capacity * 2
        new_buckets: list[Optional[list[Any]]] = [None] * new_capacity

        for bucket in self.buckets:
            if bucket is not None:
                for node in bucket:
                    index = node.hash % new_capacity
                    if new_buckets[index] is None:
                        new_buckets[index] = []
                    new_buckets[index].append(node)

        self.buckets = new_buckets
        self.capacity = new_capacity

    def _get_index(self, key: Any) -> int:
        return hash(key) % self.capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.size / self.capacity > self.load_factor:
            self._resize()

        index = self._get_index(key)
        if self.buckets[index] is None:
            self.buckets[index] = []

        bucket = self.buckets[index]

        for node in bucket:
            if node.key == key:
                node.value = value
                return

        node = self.Node(key, value)
        bucket.append(node)
        self.size += 1

    def __getitem__(self, key: Any) -> Any:
        index = self._get_index(key)
        bucket = self.buckets[index]

        if bucket is not None:
            for node in bucket:
                if node.key == key:
                    return node.value

        raise KeyError(f"Key '{key}' not found.")

    def __len__(self) -> int:
        return self.size

    def clear(self) -> None:
        self.buckets = [None] * self.capacity
        self.size = 0

    def __delitem__(self, key: Any) -> None:
        index = self._get_index(key)
        bucket = self.buckets[index]

        if bucket is not None:
            for index, node in enumerate(bucket):
                if node.key == key:
                    del bucket[index]
                    self.size -= 1
                    return

        raise KeyError(f"Key '{key}' not found.")

    def get(self, key: Any, default: Optional[Any] = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: Any, default: Optional[Any] = None) -> Any:
        index = self._get_index(key)
        bucket = self.buckets[index]

        if bucket is not None:
            for index, node in enumerate(bucket):
                if node.key == key:
                    value = node.value
                    del bucket[index]
                    self.size -= 1
                    return value

        if default is not None:
            return default

        raise KeyError(f"Key '{key}' not found.")

    def update(self, other: dict) -> None:
        for key, value in other.items():
            self[key] = value

    def __iter__(self) -> Iterator[Any]:
        for bucket in self.buckets:
            if bucket is not None:
                for node in bucket:
                    yield node.key
