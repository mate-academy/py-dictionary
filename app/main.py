from typing import Optional


class Node:
    """Node in the hash table storing key, hash, and value."""
    __slots__ = ("key", "hash", "value", "next")

    def __init__(self, key: object, value: object, hash_: int) -> None:
        self.key: object = key
        self.value: object = value
        self.hash: int = hash_
        self.next: Optional["Node"] = None


class Dictionary:
    """Custom dictionary implementation using hash table with chaining."""

    def __init__(
        self, initial_capacity: int = 8, load_factor: float = 0.75
    ) -> None:
        self._capacity: int = initial_capacity
        self._size: int = 0
        self._load_factor: float = load_factor
        self._buckets: list[Optional[Node]] = [
            None
            for _ in range(self._capacity)
        ]

    def __len__(self) -> int:
        return self._size

    def _bucket_index(self, key_hash: int) -> int:
        return key_hash % self._capacity

    def __setitem__(self, key: object, value: object) -> None:
        key_hash: int = hash(key)
        index: int = self._bucket_index(key_hash)
        node: Optional[Node] = self._buckets[index]

        while node:
            if node.hash == key_hash and node.key == key:
                node.value = value
                return
            node = node.next

        new_node: Node = Node(key, value, key_hash)
        new_node.next = self._buckets[index]
        self._buckets[index] = new_node
        self._size += 1

        if self._size / self._capacity > self._load_factor:
            self._resize()

    def __getitem__(self, key: object) -> object:
        key_hash: int = hash(key)
        index: int = self._bucket_index(key_hash)
        node: Optional[Node] = self._buckets[index]

        while node:
            if node.hash == key_hash and node.key == key:
                return node.value
            node = node.next

        raise KeyError(key)

    def _resize(self) -> None:
        old_buckets: list[Optional[Node]] = self._buckets
        self._capacity *= 2
        self._buckets = [
            None
            for _ in range(self._capacity)
        ]
        self._size = 0

        for head in old_buckets:
            node: Optional[Node] = head
            while node:
                self[node.key] = node.value
                node = node.next
