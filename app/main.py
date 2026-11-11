from collections.abc import Iterator
from typing import Any

INITIAL_CAPACITY = 8
LOAD_FACTOR = 0.75
RESIZE_MULTIPLIER = 2

DELETED = object()
MISSING = object()


class Node:
    def __init__(self, key: Any, key_hash: int, value: Any) -> None:
        self.key = key
        self.hash = key_hash
        self.value = value


class Dictionary:
    def __init__(self) -> None:
        self.capacity = INITIAL_CAPACITY
        self.load_factor = LOAD_FACTOR
        self.size = 0
        self.deleted_count = 0
        self.hash_table: list[Any] = [None] * self.capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        index = self._find_index(key)

        if index is not None:
            self.hash_table[index].value = value
            return

        used_slots = self.size + self.deleted_count + 1
        if used_slots > self.capacity * self.load_factor:
            self._resize()

        self._insert_node(Node(key, hash(key), value))

    def __getitem__(self, key: Any) -> Any:
        index = self._find_index(key)

        if index is None:
            raise KeyError(key)

        return self.hash_table[index].value

    def __len__(self) -> int:
        return self.size

    def __delitem__(self, key: Any) -> None:
        index = self._find_index(key)

        if index is None:
            raise KeyError(key)

        self.hash_table[index] = DELETED
        self.size -= 1
        self.deleted_count += 1

    def __iter__(self) -> Iterator[Any]:
        for node in self.hash_table:
            if isinstance(node, Node):
                yield node.key

    def clear(self) -> None:
        self.capacity = INITIAL_CAPACITY
        self.size = 0
        self.deleted_count = 0
        self.hash_table = [None] * self.capacity

    def get(self, key: Any, default: Any = None) -> Any:
        index = self._find_index(key)

        if index is None:
            return default

        return self.hash_table[index].value

    def pop(self, key: Any, default: Any = MISSING) -> Any:
        index = self._find_index(key)

        if index is None:
            if default is MISSING:
                raise KeyError(key)
            return default

        removed_value = self.hash_table[index].value
        del self[key]

        return removed_value

    def update(self, other: Any = (), **kwargs: Any) -> None:
        if isinstance(other, (Dictionary, dict)):
            for key in other:
                self[key] = other[key]
        else:
            for key, value in other:
                self[key] = value

        for key, value in kwargs.items():
            self[key] = value

    def _find_index(self, key: Any) -> int | None:
        key_hash = hash(key)
        index = key_hash % self.capacity

        for _ in range(self.capacity):
            node = self.hash_table[index]

            if node is None:
                return None

            if (
                node is not DELETED
                and node.hash == key_hash
                and node.key == key
            ):
                return index

            index = (index + 1) % self.capacity

        return None

    def _insert_node(self, node: Node) -> None:
        index = node.hash % self.capacity

        while isinstance(self.hash_table[index], Node):
            index = (index + 1) % self.capacity

        if self.hash_table[index] is DELETED:
            self.deleted_count -= 1

        self.hash_table[index] = node
        self.size += 1

    def _resize(self) -> None:
        old_table = self.hash_table

        self.capacity *= RESIZE_MULTIPLIER
        self.hash_table = [None] * self.capacity
        self.size = 0
        self.deleted_count = 0

        for node in old_table:
            if isinstance(node, Node):
                self._insert_node(node)
