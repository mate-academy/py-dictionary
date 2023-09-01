from typing import Any, Optional


class Dictionary:
    def __init__(self,
                 initial_capacity: int = 16,
                 load_factor: float = 0.75
                 ) -> None:
        self.capacity: int = initial_capacity
        self.load_factor: float = load_factor
        self.size: int = 0
        self.buckets: list[Optional[Node]] = [None] * self.capacity

    def _hash_function(self, key: Any) -> int:
        return hash(key) % self.capacity

    def _resize(self, new_capacity: int) -> None:
        old_buckets = self.buckets
        self.buckets = [None] * new_capacity
        self.capacity = new_capacity
        self.size = 0

        for node in old_buckets:
            while node:
                self[node.key] = node.value
                node = node.next

    def __setitem__(self, key: Any, value: Any) -> None:
        hash_key = self._hash_function(key)
        new_node = Node(key, hash_key, value)

        if self.buckets[hash_key] is None:
            self.buckets[hash_key] = new_node
        else:
            current = self.buckets[hash_key]
            while current:
                if current.key == key:
                    current.value = value
                    return
                if current.next is None:
                    break
                current = current.next
            current.next = new_node

        self.size += 1
        if self.size / self.capacity >= self.load_factor:
            self._resize(self.capacity * 2)

    def __getitem__(self, key: int) -> None:
        hash_key = self._hash_function(key)
        current = self.buckets[hash_key]

        while current:
            if current.key == key:
                return current.value
            current = current.next

        raise KeyError(key)

    def __len__(self) -> int:
        return self.size


class Node:
    def __init__(self, key: Any, hash_key: int, value: Any) -> None:
        self.key: Any = key
        self.hash_key: int = hash_key
        self.value: Any = value
        self.next: Optional[Node] = None
