from typing import Any, List, Optional


class Node:
    def __init__(self, key: Any, value: Any) -> None:
        self.key: Any = key
        self.value: Any = value
        self.hash_value: int = hash(key)

    def __repr__(self) -> str:
        return f"{self.key}: {self.value}"


class Dictionary:
    def __init__(
            self,
            initial_capacity: int = 8,
            load_factor: float = 0.75
    ) -> None:
        self.capacity: int = initial_capacity
        self.load_factor: float = load_factor
        self.size: int = 0
        self.buckets: List[List[Node]] = [[] for _ in range(self.capacity)]

    def _get_bucket_index(
            self,
            key: Any,
            capacity: Optional[int] = None
    ) -> int:
        cap = capacity if capacity is not None else self.capacity
        return hash(key) % cap

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.size / self.capacity >= self.load_factor:
            self._resize()

        index = self._get_bucket_index(key)
        bucket = self.buckets[index]

        for node in bucket:
            if node.key == key:
                node.value = value
                return

        new_node = Node(key, value)
        bucket.append(new_node)
        self.size += 1

    def __getitem__(self, key: Any) -> Any:
        index = self._get_bucket_index(key)
        bucket = self.buckets[index]

        for node in bucket:
            if node.key == key:
                return node.value

        raise KeyError(f"Key '{key}' not found.")

    def __len__(self) -> int:
        return self.size

    def _resize(self) -> None:
        new_capacity = self.capacity * 2
        new_buckets: List[List[Node]] = [[] for _ in range(new_capacity)]

        for bucket in self.buckets:
            for node in bucket:
                new_index = node.hash_value % new_capacity
                new_buckets[new_index].append(node)

        self.capacity = new_capacity
        self.buckets = new_buckets
