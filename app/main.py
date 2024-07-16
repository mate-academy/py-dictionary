from typing import Hashable, Any


class Node:
    def __init__(self, key: Hashable, value: Any) -> None:
        self.key = key
        self.value = value
        self.hash = hash(key)

    def __repr__(self) -> str:
        return f"{self.key}: {self.value}"


class Dictionary:
    def __init__(
            self,
            initial_capacity: int = 8,
            load_factor: float = 0.66
    ) -> None:
        self.capacity = initial_capacity
        self.load_factor = load_factor
        self.size = 0
        self.buckets = [None] * self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if isinstance(key, (list, dict)):
            raise KeyError(f"Invalid key: {key}]")

        if self.size / self.capacity >= self.load_factor:
            self._resize()

        index = hash(key) % self.capacity
        if not self.buckets[index]:
            self.buckets[index] = []

        for node in self.buckets[index]:
            if node.key == key:
                node.value = value
                return

        self.buckets[index].append(Node(key, value))
        self.size += 1

    def __getitem__(self, key: Hashable) -> Any:
        index = hash(key) % self.capacity
        if self.buckets[index]:
            for node in self.buckets[index]:
                if node.key == key:
                    return node.value
        raise KeyError(f"Key {key} not found")

    def __len__(self) -> int:
        return self.size

    def _resize(self) -> None:
        new_capacity = self.capacity * 2
        new_buckets = [None] * new_capacity

        for bucket in self.buckets:
            if bucket:
                for node in bucket:
                    index = node.hash % new_capacity
                    if not new_buckets[index]:
                        new_buckets[index] = []
                    new_buckets[index].append(node)

    def clear(self) -> None:
        self.capacity = 8
        self.size = 0
        self.buckets = [None] * self.capacity

    def __repr__(self) -> str:
        return "\n".join(
            [str(bucket) for bucket in self.buckets if bucket is not None]
        )
