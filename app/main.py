from typing import Any, Hashable, Iterator


class Node:
    def __init__(self, key: Hashable, key_hash: int, value: Any) -> None:
        self.key = key
        self.hash = key_hash
        self.value = value


# Marks a slot whose node was deleted, so probing continues past it
_DELETED = object()
_MISSING = object()


class Dictionary:
    INITIAL_CAPACITY = 8
    LOAD_FACTOR = 2 / 3
    RESIZE_MULTIPLIER = 2

    def __init__(self) -> None:
        self.length = 0
        self.deleted = 0
        self.capacity = self.INITIAL_CAPACITY
        self.hash_table: list = [None] * self.capacity

    def _find_index(self, key: Hashable, key_hash: int) -> int:
        """Return the slot index holding the key, or the slot to insert it."""
        index = key_hash % self.capacity
        first_deleted = None
        while True:
            node = self.hash_table[index]
            if node is None:
                return first_deleted if first_deleted is not None else index
            if node is _DELETED:
                if first_deleted is None:
                    first_deleted = index
            elif node.hash == key_hash and node.key == key:
                return index
            index = (index + 1) % self.capacity

    def _resize(self) -> None:
        if self.length + 1 > self.capacity * self.LOAD_FACTOR:
            self.capacity *= self.RESIZE_MULTIPLIER
        old_table = self.hash_table
        self.hash_table = [None] * self.capacity
        self.deleted = 0
        for node in old_table:
            if node is not None and node is not _DELETED:
                self.hash_table[self._find_index(node.key, node.hash)] = node

    def __setitem__(self, key: Hashable, value: Any) -> None:
        key_hash = hash(key)
        index = self._find_index(key, key_hash)
        node = self.hash_table[index]
        if node is not None and node is not _DELETED:
            node.value = value
            return

        if self.length + self.deleted + 1 > self.capacity * self.LOAD_FACTOR:
            self._resize()
            index = self._find_index(key, key_hash)
        elif node is _DELETED:
            self.deleted -= 1

        self.hash_table[index] = Node(key, key_hash, value)
        self.length += 1

    def _get_node_index(self, key: Hashable) -> int:
        index = self._find_index(key, hash(key))
        node = self.hash_table[index]
        if node is None or node is _DELETED:
            raise KeyError(f"Key {key!r} is not in the dictionary")
        return index

    def __getitem__(self, key: Hashable) -> Any:
        return self.hash_table[self._get_node_index(key)].value

    def __delitem__(self, key: Hashable) -> None:
        index = self._get_node_index(key)
        self.hash_table[index] = _DELETED
        self.length -= 1
        self.deleted += 1

    def __len__(self) -> int:
        return self.length

    def __contains__(self, key: Hashable) -> bool:
        try:
            self._get_node_index(key)
        except KeyError:
            return False
        return True

    def __iter__(self) -> Iterator:
        for node in self.hash_table:
            if node is not None and node is not _DELETED:
                yield node.key

    def clear(self) -> None:
        self.__init__()

    def get(self, key: Hashable, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: Hashable, default: Any = _MISSING) -> Any:
        try:
            value = self[key]
        except KeyError:
            if default is _MISSING:
                raise
            return default
        del self[key]
        return value

    def update(self, other: Any = (), **kwargs) -> None:
        if hasattr(other, "keys"):
            for key in other.keys():
                self[key] = other[key]
        else:
            for key, value in other:
                self[key] = value
        for key, value in kwargs.items():
            self[key] = value

    def keys(self) -> list:
        return list(self)
