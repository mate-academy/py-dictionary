from typing import Any, Iterator


class _Node:
    """
    Stores one key-value pair together with the pre-computed hash.
    Caching the hash avoids recomputing it during resize operations.
    """
    __slots__ = ("key", "hash", "value")

    def __init__(self, key: Any, hash_val: int, value: Any) -> None:
        self.key = key
        self.hash = hash_val
        self.value = value

    def __repr__(self) -> str:
        return f"Node(key={self.key!r}, value={self.value!r})"


class Dictionary:
    """
    Hash-table dictionary with separate chaining for collision resolution.
    """

    INITIAL_CAPACITY = 8
    MAX_LOAD_FACTOR = 0.75
    GROW_FACTOR = 2

    def __init__(self) -> None:
        self._capacity = self.INITIAL_CAPACITY
        self._size = 0
        self._buckets: list[list[_Node]] = [[] for _ in range(self._capacity)]

    def _bucket_index(self, hash_val: int) -> int:
        """Map an arbitrary hash value to a valid bucket index."""
        return hash_val % self._capacity

    def _load_factor(self) -> float:
        return self._size / self._capacity

    def _find_node(self, key: Any, hash_val: int) -> _Node | None:
        """
        Return the _Node for *key* inside the appropriate bucket, or None.
        We compare both the cached hash AND the key itself so that two keys
        with the same hash are never confused.
        """
        chain = self._buckets[self._bucket_index(hash_val)]
        for node in chain:
            if node.hash == hash_val and node.key == key:
                return node
        return None

    def _resize(self) -> None:
        """
        Double capacity and rehash every existing node into the new table.
        This is O(n) but happens infrequently.
        """
        old_buckets = self._buckets
        self._capacity *= self.GROW_FACTOR
        self._buckets = [[] for _ in range(self._capacity)]
        self._size = 0

        for chain in old_buckets:
            for node in chain:
                self[node.key] = node.value

    def __setitem__(self, key: Any, value: Any) -> None:
        h = hash(key)
        node = self._find_node(key, h)
        if node is not None:
            node.value = value
            return

        if self._load_factor() >= self.MAX_LOAD_FACTOR:
            self._resize()

        idx = self._bucket_index(h)
        self._buckets[idx].append(_Node(key, h, value))
        self._size += 1

    def __getitem__(self, key: Any) -> Any:
        h = hash(key)
        node = self._find_node(key, h)
        if node is None:
            raise KeyError(key)
        return node.value

    def __len__(self) -> int:
        return self._size

    def __delitem__(self, key: Any) -> None:
        h = hash(key)
        idx = self._bucket_index(h)
        chain = self._buckets[idx]
        for i, node in enumerate(chain):
            if node.key == key and node.hash == h:
                del chain[i]
                self._size -= 1
                return
        raise KeyError(key)

    def __contains__(self, key: Any) -> bool:
        h = hash(key)
        return self._find_node(key, h) is not None

    def __iter__(self) -> Iterator:
        for chain in self._buckets:
            for node in chain:
                yield node.key

    def __repr__(self) -> str:
        pairs = ", ".join(
            f"{node.key!r}: {node.value!r}"
            for chain in self._buckets
            for node in chain
        )
        return f"Dictionary({{{pairs}}})"

    def __str__(self) -> str:
        pairs = ", ".join(
            f"{node.key!r}: {node.value!r}"
            for chain in self._buckets
            for node in chain
        )
        return "{" + pairs + "}"

    def get(self, key: Any, default: Any = None) -> Any:
        h = hash(key)
        node = self._find_node(key, h)
        return node.value if node is not None else default

    def pop(self, key: Any, *args: Any) -> Any:
        h = hash(key)
        idx = self._bucket_index(h)
        chain = self._buckets[idx]

        for i, node in enumerate(chain):
            if node.hash == h and node.key == key:
                del chain[i]
                self._size -= 1
                return node.value

        if args:
            return args[0]
        raise KeyError(key)

    def update(self, other: Any = None, **kwargs: Any) -> None:
        if other is not None:
            it = other.items() if hasattr(other, "items") else other
            for k, v in it:
                self[k] = v
        for k, v in kwargs.items():
            self[k] = v

    def clear(self) -> None:
        self._capacity = self.INITIAL_CAPACITY
        self._buckets = [[] for _ in range(self._capacity)]
        self._size = 0

    def keys(self) -> list:
        return list(self)

    def values(self) -> list:
        return [node.value for chain in self._buckets for node in chain]

    def items(self) -> list[tuple]:
        return [(node.key, node.value)
                for chain in self._buckets
                for node in chain]
