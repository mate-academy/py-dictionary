from typing import Any, List


class Node:
    def __init__(self, key: Any, value: Any) -> None:
        self.key: Any = key
        self.hash: int = hash(key)
        self.value: Any = value

    def __repr__(self) -> str:
        return f"Node({self.key}: {self.value})"


class Dictionary:
    def __init__(
            self,
            initial_capacity: int = 8,
            load_factor_threshold: float = 0.75
    ) -> None:
        self.capacity: int = initial_capacity
        self.size: int = 0
        self.load_factor_threshold: float = load_factor_threshold
        self.buckets: List[List[Node]] = [[] for _ in range(self.capacity)]

    def _get_index(self, key_hash: int) -> int:
        return key_hash % self.capacity

    def _resize(self) -> None:
        old_buckets: List[List[Node]] = self.buckets
        self.capacity *= 2
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0

        for bucket in old_buckets:
            for node in bucket:
                self[node.key] = node.value

    def __setitem__(self, key: Any, value: Any) -> None:
        key_hash: int = hash(key)
        index: int = self._get_index(key_hash)
        bucket: List[Node] = self.buckets[index]

        for node in bucket:
            if node.key == key:
                node.value = value
                return

        bucket.append(Node(key, value))
        self.size += 1

        if self.size / self.capacity > self.load_factor_threshold:
            self._resize()

    def __getitem__(self, key: Any) -> Any:
        key_hash: int = hash(key)
        index: int = self._get_index(key_hash)
        bucket: List[Node] = self.buckets[index]

        for node in bucket:
            if node.key == key:
                return node.value

        raise KeyError(f"Key '{key}' not found.")

    def __len__(self) -> int:
        return self.size

    def __repr__(self) -> str:
        pairs = (f"{node.key}: {node.value}"
                 for bucket in self.buckets for node in bucket)
        return "{" + ", ".join(pairs) + "}"
