from typing import Any, Optional, Iterator


class Dictionary:
    class _Node:
        def __init__(self, key: Any, value: Any) -> None:
            self.key = key
            self.value = value
            self.next = None

    def __init__(self, initial_capacity: int = 16) -> None:
        self.capacity: int = initial_capacity
        self.size: int = 0
        self.table: list[Optional[self._Node]] = [None] * self.capacity

    def _hash(self, key: Any) -> int:
        """Generate a hash for the key."""
        return hash(key) % self.capacity

    def _resize(self) -> None:
        """Resize the hash table when the load factor is exceeded."""
        self.capacity *= 2
        new_table: list[Optional[self._Node]] = [None] * self.capacity

        for node in self.table:
            while node:
                index = self._hash(node.key)
                new_node = self._Node(node.key, node.value)

                new_node.next = new_table[index]
                new_table[index] = new_node

                node = node.next

        self.table = new_table

    def __setitem__(self, key: Any, value: Any) -> None:
        """Insert or update a key-value pair."""
        index = self._hash(key)
        node = self.table[index]
        while node:
            if node.key == key:
                node.value = value
                return
            node = node.next

        new_node = self._Node(key, value)
        new_node.next = self.table[index]
        self.table[index] = new_node
        self.size += 1

        # Check if resizing is needed
        if self.size / self.capacity > 0.75:
            self._resize()

    def __getitem__(self, key: Any) -> Any:
        """Retrieve the value associated with the key."""
        index = self._hash(key)
        node = self.table[index]
        while node:
            if node.key == key:
                return node.value
            node = node.next
        raise KeyError(f"Key {key} not found.")

    def __len__(self) -> int:
        """Return the number of key-value pairs in the dictionary."""
        return self.size

    def clear(self) -> None:
        """Remove all items from the dictionary."""
        self.table = [None] * self.capacity
        self.size = 0

    def __delitem__(self, key: Any) -> None:
        """Delete a key-value pair from the dictionary."""
        index = self._hash(key)
        node = self.table[index]
        prev = None
        while node:
            if node.key == key:
                if prev:
                    prev.next = node.next
                else:
                    self.table[index] = node.next
                self.size -= 1
                return
            prev = node
            node = node.next
        raise KeyError(f"Key {key} not found.")

    def get(self, key: Any, default: Any = None) -> Any:
        """Return the value for the key, or a default value if not found."""
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: Any, default: Any = None) -> Any:
        index = self._hash(key)
        node = self.table[index]
        prev = None
        while node:
            if node.key == key:
                if prev:
                    prev.next = node.next
                else:
                    self.table[index] = node.next
                self.size -= 1
                return node.value
            prev = node
            node = node.next
        if default is not None:
            return default
        raise KeyError(f"Key {key} not found.")

    def __iter__(self) -> Iterator[Any]:
        """Iterate over the keys in the dictionary."""
        for node in self.table:
            while node:
                yield node.key
                node = node.next
