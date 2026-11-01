from typing import Any, Hashable, Iterator


class Node:
    def __init__(self, key: Hashable, key_hash: int, value: Any) -> None:
        self.key = key
        self.hash = key_hash
        self.value = value


_MISSING = object()


class Dictionary:
    def __init__(
        self,
        capacity: int = 8,
        load_factor: float = 2 / 3,
    ) -> None:
        self._capacity = capacity
        self._load_factor = load_factor
        self._size = 0
        self._table: list = [None] * capacity

    def _find_index(self, key: Hashable, key_hash: int) -> int:
        index = key_hash % self._capacity
        while self._table[index] is not None:
            node = self._table[index]
            if node.hash == key_hash and node.key == key:
                return index
            index = (index + 1) % self._capacity
        return index

    def _resize(self) -> None:
        old_nodes = [node for node in self._table if node is not None]
        self._capacity *= 2
        self._table = [None] * self._capacity
        for node in old_nodes:
            index = self._find_index(node.key, node.hash)
            self._table[index] = node

    def __setitem__(self, key: Hashable, value: Any) -> None:
        key_hash = hash(key)
        index = self._find_index(key, key_hash)

        if self._table[index] is not None:
            self._table[index].value = value
            return

        if self._size + 1 > self._capacity * self._load_factor:
            self._resize()
            index = self._find_index(key, key_hash)

        self._table[index] = Node(key, key_hash, value)
        self._size += 1

    def __getitem__(self, key: Hashable) -> Any:
        index = self._find_index(key, hash(key))
        if self._table[index] is None:
            raise KeyError(key)
        return self._table[index].value

    def __len__(self) -> int:
        return self._size

    def __delitem__(self, key: Hashable) -> None:
        index = self._find_index(key, hash(key))
        if self._table[index] is None:
            raise KeyError(key)

        self._table[index] = None
        self._size -= 1

        next_index = (index + 1) % self._capacity
        while self._table[next_index] is not None:
            node = self._table[next_index]
            self._table[next_index] = None
            new_index = self._find_index(node.key, node.hash)
            self._table[new_index] = node
            next_index = (next_index + 1) % self._capacity

    def __iter__(self) -> Iterator:
        for node in self._table:
            if node is not None:
                yield node.key

    def __contains__(self, key: Hashable) -> bool:
        return self._table[self._find_index(key, hash(key))] is not None

    def __repr__(self) -> str:
        items = ", ".join(
            f"{node.key!r}: {node.value!r}"
            for node in self._table
            if node is not None
        )
        return "{" + items + "}"

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

    def clear(self) -> None:
        self._table = [None] * self._capacity
        self._size = 0

    def update(self, other: Any) -> None:
        if hasattr(other, "keys") or isinstance(other, Dictionary):
            for key in other:
                self[key] = other[key]
        else:
            for key, value in other:
                self[key] = value
