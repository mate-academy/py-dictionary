from __future__ import annotations
from typing import Any
from dataclasses import dataclass


@dataclass()
class Node:
    key: Any
    key_hash: int
    value: Any


class ResizeManager:
    def __init__(
            self,
            dictionary: Dictionary
    ) -> None:
        self.dictionary = dictionary

    def __enter__(self) -> None:
        self.dictionary.ACTUAL_CAPACITY *= 2
        old_table = self.dictionary.hash_table
        new_table = [None] * self.dictionary.ACTUAL_CAPACITY
        self.dictionary.hash_table = new_table
        self.dictionary.threshold = round(
            len(self.dictionary.hash_table) / 3 * 2
        )

        for node in old_table:
            if node:
                index = node.key_hash % self.dictionary.ACTUAL_CAPACITY
                while self.dictionary.hash_table[index] is not None:
                    index = (index + 1) % self.dictionary.ACTUAL_CAPACITY
                self.dictionary.hash_table[index] = node

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        pass


class Dictionary:
    def __init__(self) -> None:
        self.ACTUAL_CAPACITY = 8
        self.hash_table = [None] * self.ACTUAL_CAPACITY
        self.threshold = round(len(self.hash_table) / 3 * 2)

    def __setitem__(
            self,
            key: Any,
            value: Any
    ) -> None:
        node = Node(key, hash(key), value)
        index = node.key_hash % self.ACTUAL_CAPACITY
        while self.hash_table[index] is not None:
            if self.hash_table[index].key == key:
                self.hash_table[index] = node
                return
            index = (index + 1) % self.ACTUAL_CAPACITY

        self.hash_table[index] = node

        if len(self) >= self.threshold:
            with ResizeManager(self):
                pass

    def __getitem__(self, key: Any) -> Any:
        key_hash = hash(key)
        index = key_hash % self.ACTUAL_CAPACITY

        while self.hash_table[index] is not None:
            if self.hash_table[index].key == key:
                return self.hash_table[index].value
            index = (index + 1) % self.ACTUAL_CAPACITY

        raise KeyError(f"Key '{key}' not in dictionary")

    def __len__(self) -> int:
        return sum(node is not None for node in self.hash_table)
