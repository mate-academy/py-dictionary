from typing import Any, List, Optional, Iterator


class Node:
    """Node to store key-value pairs in the hash table."""
    def __init__(self, key: Any, value: Any) -> None:
        self.key: Any = key
        self.value: Any = value
        self.hash: int = hash(key)
        self.next: Optional[Node] = None
        # For handling collisions using chaining


class Dictionary:
    """Custom implementation of a dictionary using a hash table."""
    def __init__(self, initial_capacity: int = 16,
                 load_factor: float = 0.75) -> None:
        self.capacity: int = initial_capacity
        self.size: int = 0
        self.load_factor: float = load_factor
        self.table: List[Optional[Node]] = [None] * self.capacity

    def _resize(self) -> None:
        """Resize the hash table when the load factor is exceeded."""
        old_table = self.table
        self.capacity *= 2
        self.table = [None] * self.capacity
        self.size = 0

        for node in old_table:
            while node:
                self[node.key] = node.value
                node = node.next

    def _get_index(self, key: Any) -> int:
        """Get the index in the hash table for a given key."""
        return hash(key) % self.capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        """Add or update a key-value pair."""
        index = self._get_index(key)
        if not self.table[index]:
            self.table[index] = Node(key, value)
        else:
            current = self.table[index]
            while current:
                if current.key == key:
                    current.value = value
                    return
                if not current.next:
                    break
                current = current.next
            current.next = Node(key, value)

        self.size += 1

        if self.size / self.capacity > self.load_factor:
            self._resize()

    def __getitem__(self, key: Any) -> Any:
        """Retrieve the value for a given key."""
        index = self._get_index(key)
        current = self.table[index]
        while current:
            if current.key == key:
                return current.value
            current = current.next
        raise KeyError(f"Key '{key}' not found.")

    def __len__(self) -> int:
        """Return the number of key-value pairs."""
        return self.size

    def __delitem__(self, key: Any) -> None:
        """Remove a key-value pair."""
        index = self._get_index(key)
        current = self.table[index]
        prev = None
        while current:
            if current.key == key:
                if prev:
                    prev.next = current.next
                else:
                    self.table[index] = current.next
                self.size -= 1
                return
            prev, current = current, current.next
        raise KeyError(f"Key '{key}' not found.")

    def clear(self) -> None:
        """Clear the dictionary."""
        self.table = [None] * self.capacity
        self.size = 0

    def __iter__(self) -> Iterator[Any]:
        """Iterate over keys."""
        for node in self.table:
            while node:
                yield node.key
                node = node.next

    def __contains__(self, key: Any) -> bool:
        """Check if a key exists in the dictionary."""
        try:
            self[key]
            return True
        except KeyError:
            return False

    def __repr__(self) -> str:
        """String representation of the dictionary."""
        pairs = []
        for node in self.table:
            while node:
                pairs.append(f"{node.key}: {node.value}")
                node = node.next
        return "{" + ", ".join(pairs) + "}"
