from typing import Any, List


class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __eq__(self, other: Any) -> bool:
        return (isinstance(other, Point)
                and self.x == other.x and self.y == other.y)

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y})"


class Node:
    def __init__(self, key: Any, value: Any) -> None:
        self.key = key
        self.hash = hash(key)
        self.value = value


class Dictionary:
    def __init__(self, capacity: int = 8) -> None:
        self.capacity: int = capacity
        self.buckets: List[List[Node]] = [[] for _ in range(capacity)]
        self.size: int = 0
        self.load_factor_threshold: float = 0.75

    def _resize(self) -> None:
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0

        for bucket in old_buckets:
            for node in bucket:
                self[node.key] = node.value

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.size / self.capacity > self.load_factor_threshold:
            self._resize()

        index = hash(key) % self.capacity
        bucket = self.buckets[index]

        for node in bucket:
            if node.key == key:
                node.value = value
                return

        bucket.append(Node(key, value))
        self.size += 1

    def __getitem__(self, key: Any) -> Any:
        index = hash(key) % self.capacity
        bucket = self.buckets[index]

        for node in bucket:
            if node.key == key:
                return node.value

        raise KeyError(f"Key {key} not found")

    def __contains__(self, key: Any) -> bool:
        index = hash(key) % self.capacity
        bucket = self.buckets[index]

        return any(node.key == key for node in bucket)

    def get(self, key: Any, default: Any = None) -> Any:
        index = hash(key) % self.capacity
        bucket = self.buckets[index]

        for node in bucket:
            if node.key == key:
                return node.value

        return default

    def keys(self) -> List[Any]:
        return [node.key for bucket in self.buckets for node in bucket]

    def __len__(self) -> int:
        return self.size
