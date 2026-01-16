from typing import Any


class Node:
    """Represents a single entry in the hash table."""

    __slots__ = ("key", "hash", "value")

    def __init__(self, key: Any, value: Any) -> None:
        self.key = key
        self.hash = hash(key)
        self.value = value

    def __repr__(self) -> str:
        return f"Node({self.key!r}: {self.value!r})"
