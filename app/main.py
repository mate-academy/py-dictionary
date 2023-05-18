from typing import Any, Iterator, Hashable
from dataclasses import dataclass


@dataclass
class Node:
    key: Hashable
    value: Any
    hash_value: int | float
    next_node: "Node" = None


class Dictionary:

    def __init__(self) -> None:
        self._length = 0
        self._capacity = 8
        self._hash_table = [None] * self._capacity

    def _get_index_and_hash(self, key: Hashable) -> tuple:
        keys_hash = hash(key)
        index = keys_hash % self._capacity
        return index, keys_hash

    def _resize(self) -> None:
        self._length = 0
        self._capacity *= 2
        old_hash_table = self._hash_table
        self._hash_table = [None] * self._capacity

        for node in old_hash_table:
            while node is not None:
                self[node.key] = node.value
                node = node.next_node

    def __getitem__(self, key: Hashable) -> None:
        index, keys_hash = self._get_index_and_hash(key)
        current = self._hash_table[index]
        while current is not None:
            if current.hash_value == keys_hash and current.key == key:
                return current.value
            current = current.next_node
        raise KeyError(f"There are no key {key}")

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self._length >= self._capacity * 2 / 3:
            self._resize()

        index, keys_hash = self._get_index_and_hash(key)

        if self._hash_table[index] is None:
            self._hash_table[index] = Node(key, value, keys_hash)
            self._length += 1
            return

        current = self._hash_table[index]
        while current is not None:
            if current.key == key:
                current.value = value
                return

            if current.next_node is None:
                break
            current = current.next_node

        current.next_node = Node(key, value, keys_hash)
        self._length += 1

    def __len__(self) -> int:
        return self._length

    def __delitem__(self, key: Hashable) -> None:
        index, _ = self._get_index_and_hash(key)

        node = self._hash_table[index]
        prev_node = None
        while node is not None:
            if node.key == key:
                if prev_node is None:
                    self._hash_table[index] = node.next_node
                else:
                    prev_node.next_node = node.next_node
                self._length -= 1
                return
            prev_node = node
            node = node.next_node
        raise KeyError(f"There are no key {key}")

    def __iter__(self) -> Iterator:
        self._index = 0
        return self

    def __next__(self) -> Any:
        while self._index < self._capacity:

            node = self._hash_table[self._index]
            self._index += 1
            if node is not None:
                return node.key, node.value
        raise StopIteration

    def clear(self) -> None:
        self._length = 0
        self._capacity = 8
        self._hash_table = [None] * self._capacity

    def get(self, key: Hashable, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: Hashable) -> Any:
        index, _ = self._get_index_and_hash(key)

        node = self._hash_table[index]
        del self[key]
        return node.value

    def update(self, other_dict: dict) -> None:

        if not isinstance(other_dict, dict):
            raise ValueError("Only accept dictionary")

        for key, value in other_dict.items():
            self[key] = value
