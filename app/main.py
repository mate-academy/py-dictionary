from typing import Any, List


class Node:
    """A node that stores a key-value pair in a hash table."""

    def __init__(self, key: Any, value: Any) -> None:
        self.key: Any = key
        self.value: Any = value
        self.hash: int = hash(key)


class Dictionary:
    """Custom implementation of a dictionary-like data structure."""

    def __init__(self, capacity: int = 8) -> None:
        self._capacity: int = capacity
        self._size: int = 0
        self._buckets: List[List[Node]] = [[] for _ in range(capacity)]

    def _get_index(self, key_hash: int) -> int:
        return key_hash % self._capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        """Add or update a key-value pair."""
        key_hash: int = hash(key)
        index: int = self._get_index(key_hash)
        bucket: List[Node] = self._buckets[index]

        for node in bucket:
            if node.key == key:
                node.value = value
                return

        bucket.append(Node(key, value))
        self._size += 1

        if self._size / self._capacity > 0.75:
            self._resize()

    def __getitem__(self, key: Any) -> Any:
        """Retrieve the value by key."""
        key_hash: int = hash(key)
        index: int = self._get_index(key_hash)
        bucket: List[Node] = self._buckets[index]

        for node in bucket:
            if node.key == key:
                return node.value
        raise KeyError(f"Key {key!r} not found.")

    def __len__(self) -> int:
        """Return number of key-value pairs."""
        return self._size

    def _resize(self) -> None:
        """Resize hash table when load factor exceeds threshold."""
        old_buckets: List[List[Node]] = self._buckets
        self._capacity *= 2
        self._buckets = [[] for _ in range(self._capacity)]
        self._size = 0

        for bucket in old_buckets:
            for node in bucket:
                self[node.key] = node.value

    def __repr__(self) -> str:
        items: List[str] = []
        for bucket in self._buckets:
            for node in bucket:
                items.append(f"{node.key!r}: {node.value!r}")
        return "{" + ", ".join(items) + "}"
