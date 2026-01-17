from typing import Hashable, Any, Optional
from dataclasses import dataclass


class Dictionary:
    INITIAL_CAPACITY = 8
    RESIZE_THRESHOLD = 2 / 3
    CAPACITY_MULTIPLIER = 2

    @dataclass
    class Node:
        key: Hashable
        value: Any
        hash_value: int

    def __init__(self) -> None:
        self.capacity = self.INITIAL_CAPACITY
        self.size = 0
        self.hash_table: list[Dictionary.Node | None] = [None] * self.capacity

    def _calculate_index(
            self,
            key: Hashable
    ) -> int:
        hash_value = hash(key)
        index = hash_value % self.capacity
        while (
            self.hash_table[index] is not None
            and self.hash_table[index].key != key
        ):
            index = (index + 1) % self.capacity
        return index

    def _resize(self) -> None:
        old_hash_table = self.hash_table
        self.capacity *= self.CAPACITY_MULTIPLIER
        self.hash_table = [None] * self.capacity
        self.size = 0

        for node in old_hash_table:
            if node is not None:
                self[node.key] = node.value

    def __setitem__(
            self,
            key: Hashable,
            value: Any
    ) -> None:
        if self.size >= self.capacity * self.RESIZE_THRESHOLD:
            self._resize()

        index = self._calculate_index(key)
        if self.hash_table[index] is None:
            self.size += 1
            self.hash_table[index] = Dictionary.Node(key, value, hash(key))
        else:
            self.hash_table[index].value = value

    def __getitem__(
            self,
            key: Hashable
    ) -> Any:
        index = self._calculate_index(key)
        if self.hash_table[index] is None:
            raise KeyError(f"Key {key} not found.")
        return self.hash_table[index].value

    def __delitem__(
            self,
            key: Hashable
    ) -> None:
        index = self._calculate_index(key)
        if self.hash_table[index] is None:
            raise KeyError(f"Key {key} not found.")
        self.hash_table[index] = None
        self.size -= 1

        next_index = (index + 1) % self.capacity
        while self.hash_table[next_index] is not None:
            node = self.hash_table[next_index]
            self.hash_table[next_index] = None
            self.size -= 1
            self[node.key] = node.value
            next_index = (next_index + 1) % self.capacity

    def get(
            self,
            key: Hashable,
            default: Optional[Any] = None
    ) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def __len__(self) -> int:
        return self.size

    def __str__(self) -> str:
        return str([node for node in self.hash_table if node is not None])

    def clear(self) -> None:
        self.hash_table = [None] * self.capacity
        self.size = 0
