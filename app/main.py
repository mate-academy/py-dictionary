from typing import Any, Iterator, Tuple, Optional, Hashable

from app.node import Node


class Dictionary:
    """
    A custom hash-table-based dictionary implementation using chaining.

    Supports basic dictionary operations such as getting, setting,
    deleting, updating, iterating, and resizing automatically when
    the load factor threshold is exceeded.
    """

    INITIAL_CAPACITY: int = 8
    LOAD_FACTOR: float = 3 / 4

    def __init__(self) -> None:
        """Initialize an empty dictionary."""
        self.capacity = self.INITIAL_CAPACITY
        self.size = 0
        self.buckets = [None] * self.capacity

    def _hash(self, key: Any) -> int:
        """
        Compute the hash value for a key.

        Args:
            key: The key to hash.

        Returns:
            The built-in Python hash of the key.
        """
        return hash(key)

    def _get_bucket_index(self, key_hash: int) -> int:
        """
        Determine the index of the bucket corresponding to a hash value.

        Args:
            key_hash: The hash of a key.

        Returns:
            The index of the bucket to place/look up the key in.
        """
        return key_hash % self.capacity

    def _resize(self) -> None:
        """
        Resize the dictionary when load factor is exceeded.

        All existing key–value pairs are rehashed and placed into a
        new bucket array of doubled capacity.
        """
        old_buckets = self.buckets

        self.capacity *= 2
        self.buckets = [None] * self.capacity
        self.size = 0

        for bucket in old_buckets:
            current = bucket
            while current:
                self.__setitem__(current.key, current.value)
                current = current.next

    def __setitem__(self, key: Any, value: Any) -> None:
        """
        Insert or update a key–value pair.

        Args:
            key: The key to insert or update.
            value: The value to associate with the key.
        """
        if self.size / self.capacity >= self.LOAD_FACTOR:
            self._resize()

        key_hash = self._hash(key)
        index = self._get_bucket_index(key_hash)

        current = self.buckets[index]
        while current:
            if current.hash == key_hash and current.key == key:
                current.value = value
                return
            current = current.next

        new_node = Node(key, key_hash, value)
        new_node.next = self.buckets[index]
        self.buckets[index] = new_node
        self.size += 1

    def __getitem__(self, key: Any) -> Any:
        """
        Retrieve the value associated with a key.

        Args:
            key: The key whose value is requested.

        Returns:
            The value associated with the key.

        Raises:
            KeyError: If the key does not exist.
        """
        key_hash = self._hash(key)
        index = self._get_bucket_index(key_hash)

        current = self.buckets[index]
        while current:
            if current.hash == key_hash and current.key == key:
                return current.value
            current = current.next

        raise KeyError(f"Key {key} not found")

    def __len__(self) -> int:
        """
        Return the number of stored key–value pairs.

        Returns:
            The dictionary size.
        """
        return self.size

    def get(self, key: Hashable, default: Any = None) -> Any:
        """
        Return the value associated with a key or a default value.

        Args:
            key: The key to search for.
            default: Value returned if key is not found.

        Returns:
            The value associated with the key, or `default` if missing.
        """
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def __delitem__(self, key: Hashable) -> None:
        """
        Remove a key–value pair.

        Args:
            key: The key to remove.

        Raises:
            KeyError: If the key is not present.
        """
        key_hash = self._hash(key)
        index = self._get_bucket_index(key_hash)

        current = self.buckets[index]
        prev: Optional[Node] = None

        while current:
            if current.hash == key_hash and current.key == key:
                if prev:
                    prev.next = current.next
                else:
                    self.buckets[index] = current.next
                self.size -= 1
                return
            prev = current
            current = current.next

        raise KeyError(f"Key {key} not found")

    def pop(self, key: Any, default: Any = None) -> Any:
        """
        Remove a key and return its value.

        Args:
            key: The key to remove.
            default: Value to return if key is not present.

        Returns:
            The removed value or `default` if key is absent.

        Raises:
            KeyError: If key is missing and no default is given.
        """
        try:
            value = self.__getitem__(key)
            self.__delitem__(key)
            return value
        except KeyError:
            if default is None:
                raise
            return default

    def clear(self) -> None:
        """Remove all key–value pairs and reset capacity to initial size."""
        self.capacity = self.INITIAL_CAPACITY
        self.size = 0
        self.buckets = [None] * self.capacity

    def update(self, other: Any) -> None:
        """
        Update dictionary with key–value pairs from another object.

        Args:
            other: Another Dictionary, mapping, or iterable of (key, value).
        """
        if isinstance(other, Dictionary):
            for key in other:
                self.__setitem__(key, other[key])
        elif hasattr(other, "items"):
            for key, value in other.items():
                self.__setitem__(key, value)
        else:
            for key, value in other:
                self.__setitem__(key, value)

    def __iter__(self) -> Iterator[Any]:
        """
        Iterate over keys in the dictionary.

        Returns:
            An iterator over keys.
        """
        for bucket in self.buckets:
            current = bucket
            while current:
                yield current.key
                current = current.next

    def keys(self) -> Iterator[Any]:
        """
        Return an iterator over the keys.

        Returns:
            An iterator of keys.
        """
        return iter(self)

    def values(self) -> Iterator[Any]:
        """
        Return an iterator over the values.

        Returns:
            An iterator of values.
        """
        for bucket in self.buckets:
            current = bucket
            while current:
                yield current.value
                current = current.next

    def items(self) -> Iterator[Tuple[Any, Any]]:
        """
        Return an iterator over key–value pairs.

        Returns:
            An iterator of (key, value) tuples.
        """
        for bucket in self.buckets:
            current = bucket
            while current:
                yield (current.key, current.value)
                current = current.next

    def __contains__(self, key: Any) -> bool:
        """
        Check whether a key is present.

        Args:
            key: The key to search for.

        Returns:
            True if key exists, False otherwise.
        """
        try:
            self.__getitem__(key)
            return True
        except KeyError:
            return False

    def __repr__(self) -> str:
        """
        Return a string representation of the dictionary.

        Returns:
            A string resembling a standard Python dict.
        """
        items = [f"{repr(k)}: {repr(v)}" for k, v in self.items()]
        return "{" + ", ".join(items) + "}"
