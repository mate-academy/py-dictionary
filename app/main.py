from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class Node:
    key: Any
    hash_value: int
    value: Any


class Dictionary:
    INITIAL_CAPACITY = 8
    LOAD_FACTOR = 0.75
    RESIZE_MULTIPLIER = 2

    def __init__(self) -> None:
        self._capacity = self.INITIAL_CAPACITY
        self._size = 0
        self._hash_table: list[Optional[Node]] = [
            None
            for _ in range(self._capacity)
        ]

    def __setitem__(self, key: Any, value: Any) -> None:
        key_hash = hash(key)
        index = self._find_index(key, key_hash)
        node = self._hash_table[index]

        if node is not None:
            node.value = value
            return

        if self._should_resize():
            self._resize()
            index = self._find_index(key, key_hash)

        self._hash_table[index] = Node(
            key=key,
            hash_value=key_hash,
            value=value,
        )
        self._size += 1

    def __getitem__(self, key: Any) -> Any:
        key_hash = hash(key)
        start_index = key_hash % self._capacity

        for step in range(self._capacity):
            index = (start_index + step) % self._capacity
            node = self._hash_table[index]

            if node is None:
                break

            if node.hash_value == key_hash and node.key == key:
                return node.value

        raise KeyError(key)

    def __len__(self) -> int:
        return self._size

    def _find_index(self, key: Any, key_hash: int) -> int:
        start_index = key_hash % self._capacity

        for step in range(self._capacity):
            index = (start_index + step) % self._capacity
            node = self._hash_table[index]

            if node is None:
                return index

            if node.hash_value == key_hash and node.key == key:
                return index

        raise RuntimeError("Hash table is full")

    def _should_resize(self) -> bool:
        future_size = self._size + 1

        return future_size / self._capacity > self.LOAD_FACTOR

    def _resize(self) -> None:
        old_hash_table = self._hash_table

        self._capacity *= self.RESIZE_MULTIPLIER
        self._hash_table = [
            None
            for _ in range(self._capacity)
        ]

        for node in old_hash_table:
            if node is not None:
                self._insert_existing_node(node)

    def _insert_existing_node(self, node: Node) -> None:
        start_index = node.hash_value % self._capacity

        for step in range(self._capacity):
            index = (start_index + step) % self._capacity

            if self._hash_table[index] is None:
                self._hash_table[index] = node
                return

        raise RuntimeError("Hash table is full")
