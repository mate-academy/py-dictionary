from collections.abc import Iterator
from dataclasses import dataclass
from typing import Any, Hashable


@dataclass(slots=True)
class Node:
    """Store a key-value pair and its precomputed hash."""

    key: Hashable
    value: Any
    hash_value: int


class _Tombstone:
    """Mark a table slot whose node has been deleted."""


_DUMMY = _Tombstone()
_MISSING = object()


class Dictionary:
    """Store key-value pairs in an open-addressed hash table."""

    _INITIAL_SIZE = 8

    def __init__(self) -> None:
        """Initialize an empty dictionary."""
        self.length = 0
        self.hash_table: list[Node | _Tombstone | None] = (
            [None] * self._INITIAL_SIZE
        )
        self.capacity = self.size * 2 // 3

    @property
    def size(self) -> int:
        """Return the current number of table slots."""
        return len(self.hash_table)

    def __len__(self) -> int:
        """Return the number of stored key-value pairs."""
        return self.length

    def __iter__(self) -> Iterator[Hashable]:
        """Yield all stored keys."""
        for node in self.hash_table:
            if isinstance(node, Node):
                yield node.key

    def __getitem__(self, key: Hashable) -> Any:
        """Return the value associated with key."""
        hash_value = hash(key)
        index, found = self._find_slot(key, hash_value)

        if not found:
            raise KeyError(f"Key {key!r} not found")

        node = self.hash_table[index]
        assert isinstance(node, Node)
        return node.value

    def __setitem__(self, key: Hashable, value: Any) -> None:
        """Add a key-value pair or replace an existing value."""
        hash_value = hash(key)
        index, found = self._find_slot(key, hash_value)

        if found:
            node = self.hash_table[index]
            assert isinstance(node, Node)
            node.value = value
            return

        new_node = Node(key, value, hash_value)
        if self.length >= self.capacity:
            self._resize()
            self._place_node(new_node)
        else:
            self.hash_table[index] = new_node
        self.length += 1

    def __delitem__(self, key: Hashable) -> None:
        """Remove key or raise KeyError when it is absent."""
        found, _ = self._remove(key)
        if not found:
            raise KeyError(f"Key {key!r} not found")

    def items(self) -> Iterator[tuple[Hashable, Any]]:
        """Yield all stored key-value pairs."""
        for node in self.hash_table:
            if isinstance(node, Node):
                yield node.key, node.value

    def clear(self) -> None:
        """Remove all key-value pairs and reset the table."""
        self.length = 0
        self.hash_table = [None] * self._INITIAL_SIZE
        self.capacity = self.size * 2 // 3

    def get(self, key: Hashable, default: Any = None) -> Any:
        """Return the value for key or default when it is absent."""
        hash_value = hash(key)
        index, found = self._find_slot(key, hash_value)

        if not found:
            return default

        node = self.hash_table[index]
        assert isinstance(node, Node)
        return node.value

    def pop(self, key: Hashable, default: Any = _MISSING) -> Any:
        """Remove key and return its value or the provided default."""
        found, value = self._remove(key)

        if found:
            return value
        if default is not _MISSING:
            return default
        raise KeyError(f"Key {key!r} not found")

    def update(self, other: Any) -> None:
        """Add key-value pairs from a mapping or iterable of pairs."""
        items_method = getattr(other, "items", None)
        source = items_method() if callable(items_method) else other

        for key, value in source:
            self[key] = value

    def _find_slot(
        self,
        key: Hashable,
        hash_value: int,
    ) -> tuple[int, bool]:
        """Return a suitable slot index and whether key was found."""
        index = hash_value % self.size
        first_tombstone: int | None = None

        for _ in range(self.size):
            node = self.hash_table[index]
            if node is None:
                free_index = (
                    first_tombstone
                    if first_tombstone is not None
                    else index
                )
                return free_index, False
            if node is _DUMMY:
                if first_tombstone is None:
                    first_tombstone = index
            elif (
                isinstance(node, Node)
                and node.hash_value == hash_value
                and node.key == key
            ):
                return index, True

            index = (index + 1) % self.size

        if first_tombstone is not None:
            return first_tombstone, False
        return -1, False

    def _place_node(self, new_node: Node) -> None:
        """Place a node into the first available slot."""
        index = new_node.hash_value % self.size
        while self.hash_table[index] is not None:
            index = (index + 1) % self.size
        self.hash_table[index] = new_node

    def _resize(self) -> None:
        """Double the table size and redistribute stored nodes."""
        old_table = self.hash_table
        self.hash_table = [None] * (self.size * 2)
        self.capacity = self.size * 2 // 3

        for node in old_table:
            if isinstance(node, Node):
                self._place_node(node)

    def _remove(self, key: Hashable) -> tuple[bool, Any]:
        """Remove key and return whether it existed and its value."""
        hash_value = hash(key)
        index, found = self._find_slot(key, hash_value)

        if not found:
            return False, None

        node = self.hash_table[index]
        assert isinstance(node, Node)
        self.hash_table[index] = _DUMMY
        self.length -= 1
        return True, node.value
