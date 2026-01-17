from typing import Any, List


class Dictionary:
    def __init__(self) -> None:
        self.capacity: int = 8
        self.size: int = 0
        self.load_factor: float = 0.75
        self.buckets: List[List[Node]] = [[] for _ in range(self.capacity)]

    def __len__(self) -> int:
        return self.size

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.size / self.capacity > self.load_factor:
            self._resize()

        index: int = self._get_index(key)
        bucket: List[Node] = self.buckets[index]

        for node in bucket:
            if node.key == key:
                node.value = value
                return

        bucket.append(Node(key, value))
        self.size += 1

    def __getitem__(self, key: Any) -> Any:
        index: int = self._get_index(key)
        bucket: List[Node] = self.buckets[index]

        for node in bucket:
            if node.key == key:
                return node.value

        raise KeyError(f"Key {key} not found.")

    def __delitem__(self, key: Any) -> None:
        index: int = self._get_index(key)
        bucket: List[Node] = self.buckets[index]

        for i, node in enumerate(bucket):
            if node.key == key:
                del bucket[i]
                self.size -= 1
                return

        raise KeyError(f"Key {key} not found.")

    def clear(self) -> None:
        self.capacity = 8
        self.size = 0
        self.buckets = [[] for _ in range(self.capacity)]

    def _get_index(self, key: Any) -> int:
        return hash(key) % self.capacity

    def _resize(self) -> None:
        old_buckets: List[List[Node]] = self.buckets
        self.capacity *= 2
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0

        for bucket in old_buckets:
            for node in bucket:
                self[node.key] = node.value


class Node:
    def __init__(self, key: Any, value: Any) -> None:
        self.key: Any = key
        self.hash: int = hash(key)
        self.value: Any = value
