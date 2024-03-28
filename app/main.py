from typing import Any, Optional


class Node:
    def __init__(self, key: Any, hash_value: int, value: Any) -> None:
        self.key: Any = key
        self.hash: int = hash_value
        self.value: Any = value
        self.next: Optional["Node"] = None


class Dictionary:
    def __init__(self, capacity: int = 8) -> None:
        self.capacity: int = capacity
        self.size: int = 0
        self.buckets: list[Optional[Node]] = [None] * self.capacity
        self.load_factor: float = 0.75

    def __setitem__(self, key: Any, value: Any) -> None:
        hash_value: int = hash(key)
        index: int = hash_value % self.capacity
        if self.buckets[index] is None:
            self.buckets[index] = Node(key, hash_value, value)
        else:
            current: Optional[Node] = self.buckets[index]
            while True:
                if current.key == key:
                    current.value = value
                    return
                if current.next is None:
                    break
                current = current.next
            current.next = Node(key, hash_value, value)
        self.size += 1
        if self.size / self.capacity > self.load_factor:
            self._resize()

    def __getitem__(self, key: Any) -> Any:
        hash_value: int = hash(key)
        index: int = hash_value % self.capacity
        current: Optional[Node] = self.buckets[index]
        while current:
            if current.key == key:
                return current.value
            current = current.next
        raise KeyError(key)

    def __len__(self) -> int:
        return self.size

    def _resize(self) -> None:
        old_buckets: list[Optional[Node]] = self.buckets
        self.capacity *= 2
        self.buckets = [None] * self.capacity
        self.size = 0
        for node in old_buckets:
            current = node
            while current:
                self[current.key] = current.value
                current = current.next
