from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class _Node:
    key: Any
    hash_value: int
    value: Any
    next_node: "_Node | None" = None


class Dictionary:
    _initial_capacity = 8
    _load_factor = 0.75

    def __init__(self) -> None:
        self.length = 0
        self.hash_table: list[_Node | None] = (
            [None] * self._initial_capacity
        )

    def __len__(self) -> int:
        return self.length

    def __setitem__(self, key: Any, value: Any) -> None:
        key_hash = hash(key)
        bucket_index = self._get_bucket_index(key_hash)
        current_node = self.hash_table[bucket_index]

        while current_node is not None:
            if (
                current_node.hash_value == key_hash
                and current_node.key == key
            ):
                current_node.value = value
                return
            current_node = current_node.next_node

        self.hash_table[bucket_index] = _Node(
            key=key,
            hash_value=key_hash,
            value=value,
            next_node=self.hash_table[bucket_index],
        )
        self.length += 1

        if self.length / len(self.hash_table) > self._load_factor:
            self._resize()

    def __getitem__(self, key: Any) -> Any:
        node = self._find_node(key)
        if node is None:
            raise KeyError(f"Key {key!r} not found")
        return node.value

    def __delitem__(self, key: Any) -> None:
        key_hash = hash(key)
        bucket_index = self._get_bucket_index(key_hash)
        current_node = self.hash_table[bucket_index]
        previous_node: _Node | None = None

        while current_node is not None:
            if (
                current_node.hash_value == key_hash
                and current_node.key == key
            ):
                if previous_node is None:
                    self.hash_table[bucket_index] = current_node.next_node
                else:
                    previous_node.next_node = current_node.next_node
                self.length -= 1
                return
            previous_node = current_node
            current_node = current_node.next_node

        raise KeyError(f"Key {key!r} not found")

    def clear(self) -> None:
        self.hash_table = [None] * self._initial_capacity
        self.length = 0

    def _find_node(self, key: Any) -> _Node | None:
        key_hash = hash(key)
        bucket_index = self._get_bucket_index(key_hash)
        current_node = self.hash_table[bucket_index]

        while current_node is not None:
            if (
                current_node.hash_value == key_hash
                and current_node.key == key
            ):
                return current_node
            current_node = current_node.next_node

        return None

    def _get_bucket_index(self, key_hash: int) -> int:
        return key_hash % len(self.hash_table)

    def _resize(self) -> None:
        old_hash_table = self.hash_table
        self.hash_table = [None] * (len(old_hash_table) * 2)

        for node in old_hash_table:
            current_node = node
            while current_node is not None:
                next_node = current_node.next_node
                bucket_index = self._get_bucket_index(
                    current_node.hash_value
                )
                current_node.next_node = self.hash_table[bucket_index]
                self.hash_table[bucket_index] = current_node
                current_node = next_node
