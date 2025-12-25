from __future__ import annotations

from fractions import Fraction
from typing import Any, Hashable


class Node:
    def __init__(
            self,
            key: Hashable,
            value: Any,
            hash_value: int,
            next_node: Node = None
    ) -> None:
        self.key = key
        self.value = value
        self.hash_value = hash_value
        self.next = next_node


class Dictionary:
    def __init__(
            self,
    ) -> None:
        self._capacity = 8
        self._load_factor = Fraction(2, 3)
        self._threshold = self._capacity * self._load_factor
        self._hash_table = [None] * self._capacity
        self._size = 0

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self._size > self._threshold:
            self._get_resized()
        calc_hash = hash(key)
        index = calc_hash % self._capacity
        node = self._hash_table[index]
        prev_node = None

        while node:
            if node.key == key:
                node.value = value
                return
            prev_node = node
            node = node.next
        new_node = Node(key, value, calc_hash)
        if prev_node is None:
            self._hash_table[index] = new_node
        else:
            prev_node.next = new_node
        self._size += 1

    def __len__(self) -> int:
        return self._size

    def __getitem__(self, key: Hashable) -> Any:
        index = hash(key) % self._capacity
        node = self._hash_table[index]
        while node:
            if node.key == key:
                return node.value
            node = node.next
        raise KeyError

    def _get_resized(self) -> None:
        self._capacity = self._capacity * 2
        self._threshold = self._capacity * self._load_factor
        copy_table = self._hash_table
        self._hash_table = [None] * self._capacity
        self._size = 0
        for node in copy_table:
            while node:
                self[node.key] = node.value
                node = node.next
