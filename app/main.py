class Node:
    """Node for storing key-value pairs in the hash table."""

    def __init__(self, key: object, value: object, node_hash: int) -> None:
        self.key = key
        self.value = value
        self.hash = node_hash
        self.next: Node | None = None


class Dictionary:
    """Custom dictionary implementation using a hash table."""

    def __init__(
        self, initial_capacity: int = 8, load_factor: float = 0.75
    ) -> None:
        self.capacity = initial_capacity
        self.load_factor = load_factor
        self.size = 0
        self.hash_table: list[Node | None] = [None] * self.capacity

    def _get_index(self, key: object) -> int:
        """Calculate the index for a key in the hash table."""
        key_hash = hash(key)
        return key_hash % self.capacity

    def __setitem__(self, key: object, value: object) -> None:
        """Add or update a key-value pair in the dictionary."""
        index = self._get_index(key)
        node = self.hash_table[index]
        key_hash = hash(key)

        while node is not None:
            if node.hash == key_hash and node.key == key:
                node.value = value
                return
            node = node.next

        new_node = Node(key, value, key_hash)
        new_node.next = self.hash_table[index]
        self.hash_table[index] = new_node
        self.size += 1

        if self.size > self.capacity * self.load_factor:
            self._resize()

    def __getitem__(self, key: object) -> object:
        """Retrieve the value associated with a key."""
        index = self._get_index(key)
        node = self.hash_table[index]
        key_hash = hash(key)

        while node is not None:
            if node.hash == key_hash and node.key == key:
                return node.value
            node = node.next

        raise KeyError(f"Key '{key}' not found")

    def __len__(self) -> int:
        """Return the number of key-value pairs in the dictionary."""
        return self.size

    def _resize(self) -> None:
        """Resize the hash table to double its current capacity."""
        old_table = self.hash_table
        self.capacity *= 2
        self.hash_table = [None] * self.capacity
        old_size = self.size
        self.size = 0

        for node in old_table:
            while node is not None:
                self[node.key] = node.value
                node = node.next

        assert self.size == old_size

    def __delitem__(self, key: object) -> None:
        """Delete a key-value pair from the dictionary."""
        index = self._get_index(key)
        node = self.hash_table[index]
        prev = None
        key_hash = hash(key)

        while node is not None:
            if node.hash == key_hash and node.key == key:
                if prev is None:
                    self.hash_table[index] = node.next
                else:
                    prev.next = node.next
                self.size -= 1
                return
            prev = node
            node = node.next

        raise KeyError(f"Key '{key}' not found")

    def clear(self) -> None:
        """Remove all key-value pairs from the dictionary."""
        self.hash_table = [None] * self.capacity
        self.size = 0

    def get(self, key: object, default: object = None) -> object:
        """Return the value for a key if it exists, else return default."""
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: object, default: object = None) -> object:
        """Remove a key-value pair and return its value."""
        try:
            value = self[key]
            del self[key]
            return value
        except KeyError:
            if default is not None:
                return default
            raise KeyError(f"Key '{key}' not found")

    def update(self, other: dict) -> None:
        """
            Update the dictionary with key-value pairs from another dictionary.
        """
        for key, value in other.items():
            self[key] = value

    def __iter__(self) -> iter:
        """Return an iterator over the keys of the dictionary."""
        for node in self.hash_table:
            while node is not None:
                yield node.key
                node = node.next
