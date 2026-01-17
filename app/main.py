from typing import Optional, Any, Iterable, List, Tuple


class Node:
    def __init__(
        self,
        key: Any,
        value: Any,
        hash_val: int,
    ) -> None:
        self.key = key
        self.value = value
        self.hash_val = hash_val
        self.next = None


class Dictionary:
    def __init__(
        self,
        other: Optional[Any] = None,
        initial_capacity: int = 8,
        max_load_factor: float = 0.7,
        **kwargs: Any,
    ) -> None:
        self.buckets: List[Optional[Node]] = [None] * initial_capacity
        self.size = 0
        self.capacity = initial_capacity
        self.max_load_factor = max_load_factor

        if other or kwargs:
            self.update(other, **kwargs)

    def __setitem__(
        self,
        key: Any,
        value: Any,
    ) -> None:
        """
        Set the value for the specified key in the dictionary.
        """
        hash_value = hash(key)
        index = hash_value % self.capacity

        # check key in chain
        node = self.buckets[index]
        while node:
            if node.key == key:
                # Key already exists, update value
                node.value = value
                return
            node = node.next

        new_node = Node(key, value, hash_value)
        new_node.next = self.buckets[index]  # Insert at the head of the chain
        self.buckets[index] = new_node  # Update bucket with new node
        self.size += 1

        # Check if resize needed
        if self.size / self.capacity > self.max_load_factor:
            self._resize()

    def __getitem__(self, key: Any) -> Any:
        """
        Retrieve the value associated with the specified key.
        """
        hash_value = hash(key)
        index = hash_value % self.capacity

        node = self.buckets[index]
        while node:
            if node.key == key:
                return node.value
            node = node.next
        raise KeyError(f"Key not found: {key}")

    def __delitem__(self, key: Any) -> None:
        """
        Remove the specified key from the dictionary.
        """
        hash_value = hash(key)
        index = hash_value % self.capacity

        prev_node = None
        node = self.buckets[index]
        while node:
            if node.key == key:
                if prev_node:
                    prev_node.next = node.next
                else:
                    self.buckets[index] = node.next
                self.size -= 1
                return
            prev_node = node
            node = node.next

    def __len__(self) -> int:
        return self.size

    def __iter__(self) -> Iterable[Any]:
        """
        Iterate over the keys in the dictionary.
        """
        for node in self.buckets:
            while node:
                yield node.key
                node = node.next

    def __repr__(self) -> str:
        """
        Return a representation of the dictionary.
        """
        return f"Dictionary({str({k: v for k, v in self.items()})})"

    def __str__(self) -> str:
        """
        Return a string representation of the dictionary.
        """
        return str({k: v for k, v in self.items()})

    def __contains__(self, key: Any) -> bool:
        """
        Check if the dictionary contains the specified key.
        """
        index = hash(key) % self.capacity
        node = self.buckets[index]
        while node:
            if node.key == key:
                return True
            node = node.next
        return False

    def _resize(self) -> None:
        """
        Resize the dictionary to double its capacity and rehash all items.
        """
        new_capacity = self.capacity * 2
        new_buckets = [None] * new_capacity

        for node in self.buckets:
            while node:
                next_node = node.next
                new_index = node.hash_val % new_capacity

                node.next = new_buckets[new_index]
                new_buckets[new_index] = node

                node = next_node

        self.buckets = new_buckets
        self.capacity = new_capacity

    def clear(self) -> None:
        """
        Clear the dictionary, removing all items.
        """
        self.buckets = [None] * self.capacity
        self.size = 0

    def get(self, key: Any, default: Optional[Any] = None) -> Any:
        """
        Return the value for key if key is in the dictionary, else default.
        """
        try:
            return self[key]
        except KeyError:
            return default

    def update(
        self,
        other: Optional[Any] = None,
        **kwargs: Any,
    ) -> None:
        """
        Update the dictionary with key/value pairs from other,
         overwriting existing keys.
        """
        if other:
            if hasattr(other, "items"):
                for key, value in other.items():
                    self[key] = value
            else:
                for key, value in other:
                    self[key] = value
        for key, value in kwargs.items():
            self[key] = value

    def pop(self, key: Any, default: Optional[Any] = None) -> Any:
        """
        Remove specified key and return the corresponding value.
        If key is not found, default is returned if given,
        otherwise KeyError is raised.
        """
        try:
            value = self[key]
            del self[key]
            return value
        except KeyError:
            if default:
                return default
            raise

    def debug_str(self) -> str:
        """Return a string showing the hash table structure (for debugging)."""
        lines = []
        for i in range(self.capacity):
            line = f"[{i}]"
            node = self.buckets[i]
            while node:
                line += f" --> {node.key}: {node.value}"
                node = node.next
            lines.append(line)
        return "\n".join(lines)

    def keys(self) -> List[Any]:
        """Return a list of keys in the dictionary."""
        return list(self.__iter__())

    def values(self) -> List[Any]:
        """Return a list of values in the dictionary."""
        values = []
        for node in self.buckets:
            while node:
                values.append(node.value)
                node = node.next
        return values

    def items(self) -> List[Tuple[Any, Any]]:
        """Return a list of key-value pairs in the dictionary."""
        items = []
        for node in self.buckets:
            while node:
                items.append((node.key, node.value))
                node = node.next
        return items
