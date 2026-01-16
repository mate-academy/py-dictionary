from typing import Any, List, Optional, Iterator, Tuple


class Node:

    def __init__(self, key: Any, value: Any, key_hash: int) -> None:
        self.key = key
        self.value = value
        self.key_hash = key_hash


class Dictionary:

    def __init__(self, initial_capacity: int = 8,
                 load_factor: float = 2 / 3) -> None:
        self.capacity = initial_capacity
        self.load_factor = load_factor
        self.size = 0
        self.buckets: List[List[Node]] = [[] for _ in range(self.capacity)]

    def _hash(self, key: Any) -> int:
        return hash(key) % self.capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        key_hash = self._hash(key)
        bucket = self.buckets[key_hash]

        for node in bucket:
            if node.key == key:
                node.value = value
                return

        bucket.append(Node(key, value, key_hash))
        self.size += 1

        if self.size / self.capacity > self.load_factor:
            self._resize()

    def __getitem__(self, key: Any) -> Any:
        key_hash = self._hash(key)
        bucket = self.buckets[key_hash]

        for node in bucket:
            if node.key == key:
                return node.value

        raise KeyError(f"Key '{key}' not found")

    def __len__(self) -> int:
        return self.size

    def _resize(self) -> None:
        new_capacity = self.capacity * 2
        new_buckets: List[List[Node]] = [[] for _ in range(new_capacity)]

        for bucket in self.buckets:
            for node in bucket:
                new_hash = hash(node.key) % new_capacity
                new_buckets[new_hash].append(node)

        self.capacity = new_capacity
        self.buckets = new_buckets

    def clear(self) -> None:
        self.size = 0
        self.buckets = [[] for _ in range(self.capacity)]

    def __delitem__(self, key: Any) -> None:
        key_hash = self._hash(key)
        bucket = self.buckets[key_hash]

        for i, node in enumerate(bucket):
            if node.key == key:
                del bucket[i]
                self.size -= 1
                return

        raise KeyError(f"Key '{key}' not found")

    def get(self, key: Any, default: Optional[Any] = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: Any) -> Any:
        value = self[key]
        del self[key]
        return value

    def update(self, other: Any) -> None:
        if isinstance(other, dict):
            for key, value in other.items():
                self[key] = value
        else:
            for key, value in other:
                self[key] = value

    def __iter__(self) -> Iterator[Any]:
        for bucket in self.buckets:
            for node in bucket:
                yield node.key

    def items(self) -> Iterator[Tuple[Any, Any]]:
        for bucket in self.buckets:
            for node in bucket:
                yield (node.key, node.value)
