from typing import Optional, Any


class Node:
    def __init__(
        self, key: Any, value: Any, hash_value: int
    ) -> None:
        self.key: Any = key
        self.value: Any = value
        self.hash: int = hash_value
        self.next: Optional["Node"] = None


class Dictionary:
    def __init__(
        self,
        initial_capacity: int = 8,
        load_factor: float = 0.75,
    ) -> None:
        self.capacity: int = initial_capacity
        self.load_factor: float = load_factor
        self.length: int = 0
        self.buckets: list[Optional[Node]] = [None] * self.capacity

    def _hash(self, key: Any) -> int:
        return hash(key) & 0x7FFFFFFF

    def _index(self, hash_value: int) -> int:
        return hash_value % self.capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        h = self._hash(key)
        idx = self._index(h)
        node = self.buckets[idx]

        while node is not None:
            if node.hash == h and node.key == key:
                node.value = value
                return
            node = node.next

        new_node = Node(key, value, h)
        new_node.next = self.buckets[idx]
        self.buckets[idx] = new_node
        self.length += 1

        if self.length / self.capacity > self.load_factor:
            self._resize()

    def __getitem__(self, key: Any) -> Any:
        h = self._hash(key)
        idx = self._index(h)
        node = self.buckets[idx]

        while node is not None:
            if node.hash == h and node.key == key:
                return node.value
            node = node.next

        raise KeyError(f"Key '{key}' not found in dictionary")

    def __len__(self) -> int:
        return self.length

    def __delitem__(self, key: Any) -> None:
        h = self._hash(key)
        idx = self._index(h)
        prev: Optional[Node] = None
        node = self.buckets[idx]

        while node is not None:
            if node.hash == h and node.key == key:
                if prev is not None:
                    prev.next = node.next
                else:
                    self.buckets[idx] = node.next
                self.length -= 1
                return
            prev = node
            node = node.next

        raise KeyError(f"Key '{key}' not found for deletion")

    def clear(self) -> None:
        self.buckets = [None] * self.capacity
        self.length = 0

    def _resize(self) -> None:
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [None] * self.capacity
        self.length = 0

        for head in old_buckets:
            node = head
            while node is not None:
                self[node.key] = node.value
                node = node.next
