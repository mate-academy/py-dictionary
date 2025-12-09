from typing import Hashable, Any


class Node:
    """
    Represents a key–value pair stored in a bucket of the hash table.

    Attributes:
        key: The key for this entry.
        hash: The precomputed hash of the key.
        value: The associated value.
        next: The next node in the chain (or None).
    """

    def __init__(self, key: Hashable, key_hash: int, value: Any) -> None:
        """
        Initialize a Node.

        Args:
            key: The key for the entry.
            key_hash: Precomputed hash of the key.
            value: The value associated with the key.
        """
        self.key: Hashable = key
        self.hash = key_hash
        self.value = value
        self.next = None
