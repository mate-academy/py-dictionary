from typing import Any, Optional, Iterator


class Dictionary:
    def __init__(self, initial_capacity: int = 8,
                 load_factor: float = 0.75) -> None:
        self.capacity = initial_capacity
        self.load_factor = load_factor
        self.size = 0
        self.buckets = [None] * self.capacity

    def _hash(self, key: Any) -> int:
        """
        Compute the hash value for a given key.

        Args:
            key (Any): The key to hash.

        Returns:
            int: The hash value (index in the buckets list).
        """
        return hash(key) % self.capacity

    def _resize(self) -> None:
        """
        Resize the hash table when the load factor is exceeded.
        """
        # Double the capacity
        self.capacity *= 2
        new_buckets = [None] * self.capacity

        # Rehash all existing key-value pairs into the new buckets
        for bucket in self.buckets:
            if bucket is not None:
                for node in bucket:
                    index = self._hash(node.key)
                    if new_buckets[index] is None:
                        new_buckets[index] = []
                    new_buckets[index].append(node)

        # Replace the old buckets with the new buckets
        self.buckets = new_buckets

    def __setitem__(self, key: Any, value: Any) -> None:
        """
        Add or update a key-value pair in the dictionary.

        Args:
            key (Any): The key to add or update.
            value (Any): The value associated with the key.
        """
        # Resize if the load factor is exceeded
        if self.size / self.capacity >= self.load_factor:
            self._resize()

        # Compute the hash index
        index = self._hash(key)

        # Initialize the bucket if it is empty
        if self.buckets[index] is None:
            self.buckets[index] = []

        # Check if the key already exists in the bucket
        for node in self.buckets[index]:
            if node.key == key:
                node.value = value
                return

        # Add a new key-value pair
        self.buckets[index].append(Node(key, value))
        self.size += 1

    def __getitem__(self, key: Any) -> Any:
        """
        Retrieve the value associated with a given key.

        Args:
            key (Any): The key to look up.

        Returns:
            Any: The value associated with the key.

        Raises:
            KeyError: If the key is not found.
        """
        index = self._hash(key)
        if self.buckets[index] is not None:
            for node in self.buckets[index]:
                if node.key == key:
                    return node.value
        raise KeyError(f"Key '{key}' not found")

    def __len__(self) -> int:
        """
        Return the number of key-value pairs in the dictionary.

        Returns:
            int: The number of key-value pairs.
        """
        return self.size

    def __delitem__(self, key: Any) -> None:
        """
        Delete a key-value pair from the dictionary.

        Args:
            key (Any): The key to delete.

        Raises:
            KeyError: If the key is not found.
        """
        index = self._hash(key)
        if self.buckets[index] is not None:
            for i, node in enumerate(self.buckets[index]):
                if node.key == key:
                    del self.buckets[index][i]
                    self.size -= 1
                    return
        raise KeyError(f"Key '{key}' not found")

    def get(self, key: Any, default: Optional[Any] = None) -> Optional[Any]:
        try:
            return self[key]
        except KeyError:
            return default

    def clear(self) -> None:
        """
        Clear all key-value pairs from the dictionary.
        """
        self.buckets = [None] * self.capacity
        self.size = 0

    def __iter__(self) -> Iterator[Any]:
        """
        Iterate over all keys in the dictionary.

        Yields:
            Any: The keys in the dictionary.
        """
        for bucket in self.buckets:
            if bucket is not None:
                for node in bucket:
                    yield node.key


class Node:
    def __init__(self, key: Any, value: Any) -> None:
        """
        Initialize a Node with a key and value.

        Args:
            key (Any): The key.
            value (Any): The value.
        """
        self.key = key
        self.value = value
