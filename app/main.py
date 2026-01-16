from typing import Any, List


class Node:
    def __init__(self, key: Any, value: Any, hash_code: int) -> None:
        self.key: Any = key
        self.value: Any = value
        self.hash_code: int = hash_code


class Dictionary:
    def __init__(self, initial_capacity: int = 8,
                 load_factor: float = 2 / 3) -> None:
        self.capacity: int = initial_capacity
        self.load_factor: float = load_factor
        self.threshold: int = int(self.capacity * self.load_factor)
        self.size: int = 0
        self.table: List[List[Node]] = [[] for _ in range(self.capacity)]

    def __len__(self) -> int:
        return self.size

    def _hash(self, key: Any) -> int:
        return hash(key) % self.capacity

    def _resize(self) -> None:
        old_table: List[List[Node]] = self.table
        self.capacity *= 2
        self.threshold = int(self.capacity * self.load_factor)
        self.table = [[] for _ in range(self.capacity)]
        self.size = 0

        for bucket in old_table:
            for node in bucket:
                self[node.key] = node.value

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.size >= self.threshold:
            self._resize()

        index: int = self._hash(key)
        bucket: List[Node] = self.table[index]

        for node in bucket:
            if node.key == key:
                node.value = value
                return

        bucket.append(Node(key, value, hash(key)))
        self.size += 1

    def __getitem__(self, key: Any) -> Any:
        index: int = self._hash(key)
        bucket: List[Node] = self.table[index]

        for node in bucket:
            if node.key == key:
                return node.value

        raise KeyError(f"Key {key} not found")

    def __contains__(self, key: Any) -> bool:
        index: int = self._hash(key)
        bucket: List[Node] = self.table[index]
        return any(node.key == key for node in bucket)
