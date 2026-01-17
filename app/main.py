from typing import Any, Iterable


class Node:
    def __init__(self, key: Any, value: Any, hash_value: int) -> None:
        self.key = key
        self.value = value
        self.hash = hash_value


class Dictionary:
    DELETED = "DELETED"

    def __init__(self) -> None:
        """Initialize the Dictionary with default capacity and load factor."""
        self.capacity = 8
        self.length = 0
        self.load_factor = 2 / 3
        self.hash_table = [None] * self.capacity

    def _hash(self, key: Any) -> int:
        """Return the hash index for a given key."""
        return hash(key) % self.capacity

    def _resize(self) -> None:
        """Resize the hash table when the load factor is exceeded."""
        old_table = self.hash_table
        self.capacity *= 2
        self.hash_table = [None] * self.capacity
        self.length = 0

        for node in old_table:
            if node and node is not self.DELETED:
                self.__setitem__(node.key, node.value)

    def __setitem__(self, key: Any, value: Any) -> None:
        """Set the value for a given key or update if key already exists."""
        index = self._hash(key)

        while self.hash_table[index]:
            if (
                    self.hash_table[index] != self.DELETED
                    and self.hash_table[index].key == key
            ):
                self.hash_table[index].value = value
                return
            index = (index + 1) % self.capacity

        node = Node(key, value, self._hash(key))
        self.hash_table[index] = node
        self.length += 1

        if self.length / self.capacity > self.load_factor:
            self._resize()

    def __getitem__(self, key: Any) -> Any:
        """Return the value associated with the given key in the dictionary."""
        index = self._hash(key)

        while self.hash_table[index]:
            if (
                    self.hash_table[index] != self.DELETED
                    and self.hash_table[index].key == key
            ):
                return self.hash_table[index].value
            index = (index + 1) % self.capacity

        raise KeyError(f"Key '{key}' not found.")

    def __len__(self) -> int:
        """Return the number of key-value pairs in the dictionary."""
        return self.length

    def __delitem__(self, key: Any) -> None:
        """Remove the specified key from the dictionary."""
        index = self._hash(key)

        while self.hash_table[index]:
            if (self.hash_table[index] is not self.DELETED
                    and self.hash_table[index].key == key):
                self.hash_table[index] = self.DELETED
                self.length -= 1
                return
            index = (index + 1) % self.capacity

        raise KeyError(f"Key '{key}' not found.")

    def clear(self) -> None:
        """Clear all items from the dictionary."""
        self.capacity = 8
        self.length = 0
        self.hash_table = [None] * self.capacity

    def get(self, key: Any, default: Any = None) -> Any:
        """Return the value for key if key is in the dict, else default."""
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: Any, default: Any = None) -> Any:
        """Remove the specified key and return the corresponding value."""
        try:
            value = self[key]
            self.__delitem__(key)
            return value
        except KeyError:
            if default:
                return default
            raise KeyError(f"Key '{key}' not found.")

    def update(self, other: dict) -> None:
        """Update the dictionary with key/value pairs from another dict."""
        for key, value in other.items():
            self[key] = value

    def __iter__(self) -> Iterable[Any]:
        """Return an iterator over the dictionary's keys."""
        for node in self.hash_table:
            if node and node is not self.DELETED:
                yield node.key
